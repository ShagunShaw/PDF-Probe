import requests
import io
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()   
chatHistory= [SystemMessage(content='''
                            You are a helpful assistant. 
                            Answer ONLY from the provided context.
                            If the context is insufficient, just say NO CONTEXT GIVEN.''')] 

def create_vector(page_url):

    # Load PDF from a URL
    url = page_url
    response = requests.get(url)
    pdf_bytes = response.content  # proper PDF bytes

    pdf_file_like = io.BytesIO(pdf_bytes)
    reader = PdfReader(pdf_file_like)
    texts = [page.extract_text() for page in reader.pages]
    full_text = "\n".join(texts)


    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks= splitter.split_text(full_text)


    # Create embeddings and store them in vector store 
    docs = [Document(page_content=text) for text in chunks]

    vector_store = Chroma(            
        collection_name=str(hash(page_url)),
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    )
    vector_store.add_documents(documents=docs)

    return vector_store


def get_response(vector_store, query):
    global chatHistory
    
    # Retrieve relevant documents based on a query
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    retrieved_documents = retriever.invoke(query=query)

    context_text= "\n\n".join(doc.page_content for doc in retrieved_documents)



    # Send it to the LLM for answer generation
    model= ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.6) 
    prompt= PromptTemplate(
        template= """
        Context: {context}
        Question: {question}
        """,
        input_variables= ["context", "question"]
    )

    final_prompt= prompt.invoke(
        {
            "context": context_text,
            "question": query
        }
    )

    chatHistory.append(HumanMessage(content=final_prompt))
    answer= model.invoke(chatHistory)
    chatHistory.append(AIMessage(content=answer.content))

    return answer.content
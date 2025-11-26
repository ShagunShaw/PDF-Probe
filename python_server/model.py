import requests
import io
from PyPDF2 import PdfReader

# Load PDF from a URL
url = "https://www.pccoer.com/bba/pdf/achievements/student/student-research-paper.pdf"
response = requests.get(url)
pdf_bytes = response.content  # proper PDF bytes

pdf_file_like = io.BytesIO(pdf_bytes)
reader = PdfReader(pdf_file_like)
texts = [page.extract_text() for page in reader.pages]
full_text = "\n".join(texts)


# Split text into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks= splitter.split_text(full_text)


# Create embeddings and store them in vector store 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

docs = [Document(page_content=text) for text in chunks]

vector_store = Chroma(            
    collection_name="example_collection",
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
)
vector_store.add_documents(documents=docs)




# Retrieve relevant documents based on a query
query = "What is LangChain?"
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

retrieved_documents = retriever.invoke(query=query)

context_text= "\n\n".join(doc.page_content for doc in retrieved_documents)



# Send it to the LLM for answer generation
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model= ChatGoogleGenerativeAI(model_name="gemini-2.5-flash", temperature=1.6) 
prompt= PromptTemplate(
    template= """
      You are a helpful assistant.
      Answer ONLY from the provided context.
      If the context is insufficient, just say DON'T KNOW.
      Context: {context}
      Question: {question}
    """,
    input_vriables= ["context", "question"]
)

final_prompt= prompt.invoke(
    {
        "context": context_text,
        "question": query
    }
)

answer= llm.invoke(final_prompt)
print(answer.content)
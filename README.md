# PDF Probe 🔍

**PDF Probe** is a RAG based AI-powered Chrome extension that allows you to interact with PDF documents directly in your browser. Ask questions about any PDF/research papers and get instant, context-aware answers powered by Google's Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Chat**: Ask questions about any PDF document and get intelligent responses
- 🌐 **Browser Integration**: Works seamlessly with PDFs opened in Chrome
- 📚 **Context-Aware**: Uses RAG (Retrieval Augmented Generation) to provide accurate answers based on document content
- 💬 **Chat History**: Maintains conversation context for follow-up questions
- 🎨 **Clean UI**: Beautiful, non-intrusive chat interface overlaid on PDF pages

## 🛠️ Tech Stack

### Backend
- **Flask** - Lightweight Python web framework for the API server
- **LangChain** - Framework for building LLM-powered applications
- **ChromaDB** - Vector database for efficient document retrieval
- **Google Generative AI (Gemini)** - LLM for generating intelligent responses
- **PyPDF2** - PDF text extraction and processing
- **Flask-CORS** - Handling cross-origin requests from the Chrome extension

### Frontend
- **Vanilla JavaScript** - Chrome extension content script
- **Chrome Extension API** - Browser integration
- **CSS3** - Custom styling for the chat interface

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Google API Key (for Gemini AI)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ShagunShaw/PDF-Probe.git
cd PDF-Probe
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv my_env
# On Windows
my_env\Scripts\activate
# On macOS/Linux
source my_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

Add your Google API key to the `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**How to get a Google API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste it into your `.env` file

### 5. Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top-right corner)
3. Click **Load unpacked**
4. Select the `chrome_extension` folder from this project
5. The extension should now appear in your extensions list

### 6. Start the Backend Server

Navigate to the `python_server` directory and run:

```bash
cd python_server
python main.py
```

You should see:
```
 * Running on http://127.0.0.1:8000
```

### 7. Use the Extension

1. Open any PDF file in Chrome (the URL should end with `.pdf`)
2. Look for the **"Ask AI 🤖"** button in the top-right corner of the page
3. Click it to open the chat interface
4. Start asking questions about the PDF!

## 📝 Example Usage

1. Open a PDF document in Chrome
2. Click "Ask AI 🤖"
3. Ask questions like:
   - "What is this document about?"
   - "Summarize the main findings"
   - "Who are the authors?"
   - "Explain section 3 in simple terms"

## 🔧 Troubleshooting

**Extension not showing up on PDF pages:**
- Make sure the URL ends with `.pdf`
- Check if the extension is enabled in `chrome://extensions/`
- Reload the extension after making changes

**Connection errors:**
- Ensure the Flask server is running on port 8000
- Check that your `.env` file has the correct API key
- Verify CORS is enabled in the Flask app

**No response from AI:**
- Check your internet connection
- Verify your Google API key is valid and has not exceeded quota
- Check the Flask terminal for error messages

## 📂 Project Structure

```
PDF-Probe/
├── chrome_extension/
│   ├── manifest.json      # Extension configuration
│   ├── content.js         # Main extension logic
│   └── content.css        # Chat interface styling
├── python_server/
│   ├── main.py           # Flask API server
│   ├── vectors.py        # Vector store and RAG logic
│   └── .env             # Environment variables (create this)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Shagun Shaw**
- GitHub: [@ShagunShaw](https://github.com/ShagunShaw)

---

Made with ❤️ using Python, LangChain, and Chrome Extensions.
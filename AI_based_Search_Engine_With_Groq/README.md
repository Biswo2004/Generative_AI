# 🔍 Smart AI Search Engine

A **Streamlit-based AI Search Engine** that allows users to explore knowledge from **Arxiv**, **Wikipedia**, and the **Web** using a conversational interface. Powered by **Groq LLM**, it supports chat-based queries with styled responses and downloadable Arxiv PDFs.

---

🎥 **Demo Preview:**  
🚀 [Smart AI Search Engine – Demo](#) *(Replace with actual link if available)*  

This demo showcases the app in action, key features, and how it enables AI-powered research and knowledge exploration.

---

## 🌟 Features

- Ask questions to an AI assistant and get answers powered by **Groq LLM**.  
- Explore content from **Wikipedia**, **DuckDuckGo web search**, and **Arxiv research papers**.  
- **Download Arxiv PDFs** directly from the app.  
- Chat interface with **custom gradient styling** for messages.  
- Maintain **chat history** and the ability to **clear it**.  
- Dynamic **Light/Dark theme** with distinct linear gradients.  
- Styled **tabs** to separate Wikipedia, DuckDuckGo, and Arxiv results.

---

## ⚠️ Notes

- Groq API key must be **valid** and start with `gsk_`.  
- Arxiv PDF downloads depend on the **availability of the paper**.  
- Wikipedia and DuckDuckGo responses are **truncated to key points** for readability.  
- Chat history and UI styling rely on **Streamlit’s session state**.  
- **Internet connection** is required for all searches and Arxiv PDF links.  
- Some API calls may take a **few seconds** depending on query complexity.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**  
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>

---

**Create & Activate a Virtual Environment:** 

`python -m venv venv && source venv/bin/activate` 
- *(Windows: `venv\Scripts\activate`)*
- *(linux/macos: `source venv/bin/activate`)*

---

**Install Dependencies:**
- `pip install -r requirements.txt`

---

**Set Up Environment Variables:** 
- Create a `.env` file in the project root and add `GROQ_API_KEY=your_groq_api_key`
---

**🚀 Running the Streamlit App:** `streamlit run app.py` 
- Enter your Groq API Key in the sidebar (must start with `gsk_`) 
- select Light or Dark theme
-  type your query
-  explore results in Wikipedia, DuckDuckGo, and Arxiv tabs.

---

**🎛️ Optional Settings:** 
- Toggle Light/Dark theme
- clear chat history via sidebar
- explore results using organized tabs for Wikipedia, DuckDuckGo, and Arxiv.

---

**🧩 Code Overview:** 
- Loads `.env` and Groq API key
- handles theme selection and chat history via sidebar
- displays chat UI with styled messages
- integrates Groq LLM for responses
- organizes results in tabs (Wikipedia, DuckDuckGo, Arxiv)
- supports Arxiv PDF downloads, and maintains session state.

---

**📄 Example Usage:**
- Ask a question like `"Explain the key points of quantum computing research"`
- View summarized responses under Wikipedia, DuckDuckGo, and Arxiv tabs
- Download Arxiv PDF if available
- Toggle Light/Dark theme for better readability.

---

**📝 Credits:** Developed by Biswojit Bal · Powered by Groq 

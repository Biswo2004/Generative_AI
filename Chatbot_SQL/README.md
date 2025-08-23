# SQL Chatbot with Langchain & Streamlit

A Streamlit app that lets you chat with either a local SQLite database or a remote MySQL database using LLM-powered agents. Easily switch database backends, and leverage Langchain + Groq for smart data queries!

🌐 **Live Demo:** [Chat with SQL DB App](https://chat-with-sqldb-metaworkforce.streamlit.app/)

## 🔥 Features

- **Chat with SQL** – Ask questions about your database in natural language
- **Switch Database** – Toggle between local SQLite (`student.db`) or remote MySQL in the sidebar
- **History/Audit Trail** – Interactions persist across session until you clear
- **API Key Input** – Securely add Groq API Key in sidebar

## 🚀 Setup & Deployment

### 1. Clone the Repo
git clone https://github.com/your-username/sql-chatbot-streamlit.git
cd sql-chatbot-streamlit

### 2. Prepare Your SQLite Database
Run the bundled script to generate `student.db`:
- python sqlite.py
> Make sure you see `student.db` in your project directory. **Commit this file to Git!**

### 3. Add Requirements
Double-check your `requirements.txt` includes:
- streamlit
- langchain
- langchain-groq
- python-dotenv
- sqlalchemy
- pymysql

### 4. Push Everything Except Secrets
Commit all your source files, including `student.db` (see `.gitignore` below).

### 5. Deploy on Streamlit Cloud
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Deploy your repo, set `app.py` as the entry point

### 6. Using the App
- Add your Groq API Key in the sidebar when running the app
- Select the database:  
  - **Local SQLite:** No setup needed if `student.db` is in repo  
  - **Remote MySQL:** Enter host, username, password (can be stored as Streamlit secrets for security)

⚠️ **Important Note on MySQL (Streamlit Cloud Limitation)**  
Since Streamlit apps are deployed on **Streamlit Cloud**, they **cannot connect to your local MySQL instance** (`localhost`, `127.0.0.1`, or custom ports like `3309`).  
To use MySQL with the cloud app, you must connect to a **cloud-hosted MySQL service** (e.g., PlanetScale, AWS RDS, Google Cloud SQL, Azure MySQL, Railway).  
If you just want to test locally, you can connect to your own MySQL on `localhost`.  
On Streamlit Cloud, only **SQLite** (bundled `student.db`) will work out of the box.  

### 7. Environment Variables / Secrets (Recommended)
For MySQL and Groq API, on Streamlit Cloud or locally, you can use secrets:
GROQ_API_KEY=your_key_here
MYSQL_HOST=host
MYSQL_USER=username
MYSQL_PASSWORD=password
MYSQL_DB=database

Update your code to read these if you want auto-fetch (optional).

### 8. Troubleshooting

- **Database connection failed:** Check you provided all fields in the sidebar. If you are on Streamlit Cloud and trying to connect to `localhost`, remember this is not supported — use SQLite or a cloud MySQL provider.  
- **student.db missing:** Run `sqlite.py`, confirm file is there and tracked by git
- **Dependency errors:** Each required lib must be in `requirements.txt`

---

## 📝 License
MIT (or your choice)

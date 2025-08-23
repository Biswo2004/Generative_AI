import streamlit as st
from pathlib import Path
from urllib.parse import quote_plus
import sqlite3
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler

# Page setup
st.set_page_config(page_title="Langchain: Chat with SQL DB", page_icon="🗄️")
st.title("🗄️ Langchain: Chat with SQL Database")

# Constants
LOCALDB = "USE_LOCALDB"
MYSQLDB = "USE_MYSQLDB"

# Sidebar inputs
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.error("Please provide your Groq API Key.")
    st.stop()

radio_option = st.sidebar.radio("Select Database", (LOCALDB, MYSQLDB))

if radio_option == MYSQLDB:
    db_url = MYSQLDB
    mysql_host = st.sidebar.text_input("Provide your SQL Host")
    mysql_user = st.sidebar.text_input("Provide your SQL User")
    mysql_password = st.sidebar.text_input("Provide your SQL Password", type="password")
    mysql_db = st.sidebar.text_input("Provide your SQL Database Name")
else:
    db_url = LOCALDB

# LLM setup
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    streaming=True
)

# Database configuration
@st.cache_resource(ttl="2h")
def configure_db(db_url, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    try:
        if db_url == LOCALDB:
            dbfilepath = (Path(__file__).parent / "student.db").absolute()
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))

        elif db_url == MYSQLDB:
            if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
                st.error("Please provide all MySQL connection details.")
                st.stop()

            encoded_password = quote_plus(mysql_password)
            connection_str = f"mysql+pymysql://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db}"
            engine = create_engine(connection_str)
            return SQLDatabase(engine)

    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

# Initialize database
db = configure_db(db_url, mysql_host, mysql_user, mysql_password, mysql_db) if db_url == MYSQLDB else configure_db(db_url)

# Agent setup
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Chat history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User query handling
user_query = st.chat_input("Ask something about your database:")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        try:
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            error_msg = f"Query failed: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)

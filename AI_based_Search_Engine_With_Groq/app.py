import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Smart AI Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Theme Selection -----------------
st.sidebar.header("🎨 Theme Selection")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
st.session_state.theme = theme

# ----------------- API Key -----------------
st.sidebar.header("🔑 Groq API Key")
api_key_input = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if "api_valid" not in st.session_state:
    st.session_state.api_valid = False

if api_key_input and api_key_input.startswith("gsk_"):
    st.session_state.api_valid = True
else:
    st.session_state.api_valid = False
    if api_key_input:
        st.sidebar.error("Invalid API Key. Must start with 'gsk_'.")

# ----------------- Gradient Definitions -----------------
if theme == "Light":
    sidebar_bg = "linear-gradient(140deg, #667eea, #764ba2, #f093fb)"
    main_bg = "linear-gradient(160deg, #74b9ff, #0984e3, #00cec9)"
    input_bg = "linear-gradient(120deg, #667eea, #764ba2, #f093fb)"
    user_msg_bg = "linear-gradient(145deg, #e8f5e8, #c8e6c9, #81c784, #4caf50)"
    assistant_msg_bg = "linear-gradient(155deg, #fff8e1, #ffecb3, #ffd54f, #ffc107)"
else:
    sidebar_bg = "linear-gradient(140deg, #1a1a2e, #16213e, #0f3460, #533483)"
    main_bg = "linear-gradient(160deg, #2d3436, #636e72, #74b9ff)"
    input_bg = "linear-gradient(120deg, #2c1810, #3d2914, #8b4513, #a0522d)"
    user_msg_bg = "linear-gradient(145deg, #1b4332, #2d6a4f, #40916c, #52b788)"
    assistant_msg_bg = "linear-gradient(155deg, #264653, #2a9d8f, #e9c46a, #f4a261)"

# ----------------- CSS (backgrounds, chat, cards etc.) -----------------
st.markdown(f"""
<style>
/* Main background */
body {{
    background: {main_bg};
    color: #000000;
}}
.main .block-container {{
    background: {main_bg};
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}}
.sidebar .sidebar-content {{
    background: {sidebar_bg} !important;
    border-radius: 20px;
    padding: 24px;
    color: #2c3e50;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
}}
.stChatFloatingInputContainer {{
    background: {main_bg} !important;
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}}
div[data-testid="stChatMessageContainer"] {{
    background: {main_bg} !important;
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    backdrop-filter: blur(5px);
}}
section[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
}}
section[data-testid="stSidebar"] > div {{
    background: {sidebar_bg} !important;
    border-radius: 20px !important;
    margin: 10px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
}}
.main > div {{
    background: {main_bg} !important;
    border-radius: 20px;
    margin: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}}
h1 {{
    {"background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb);" if theme=="Light" else "background: linear-gradient(90deg, #00d2ff, #3a7bd5, #6a3093);"}
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}}
.subtitle {{
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
    color: #2c3e50;
    font-weight: 500;
}}
div[data-testid="stChatMessage"] {{
    border-radius: 20px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 15px;
    animation: slideUp 0.6s ease-out;
    border: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}}
div[data-testid="stChatMessage"][data-role="user"] {{
    background: {user_msg_bg} !important;
    color: #ffffff !important;
    padding-left: 60px !important;
    border: 2px solid rgba(76, 175, 80, 0.3);
    transform: translateX(-5px);
}}
div[data-testid="stChatMessage"][data-role="assistant"] {{
    background: {assistant_msg_bg} !important;
    color: #2c3e50 !important;
    padding-left: 60px !important;
    position: relative;
    border: 2px solid rgba(255, 193, 7, 0.3);
    transform: translateX(5px);
}}
div[data-testid="stChatMessage"][data-role="assistant"]::before {{
    content: url('https://i.ibb.co/S6Y0KJ7/ai-avatar.png');
    position: absolute;
    left: 10px;
    top: 10px;
    width: 40px;
    height: 40px;
}}
div[data-testid="stTextInput"] input {{
    border-radius: 30px;
    padding: 16px 24px;
    font-size: 16px;
    background: {input_bg};
    border: 2px solid rgba(255,255,255,0.2);
    color: #2c3e50;
    font-weight: 500;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}}
div[data-testid="stTextInput"] input:focus {{
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}}
div.stButton button {{
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    color: white;
    font-weight: 600;
    border-radius: 25px;
    padding: 12px 30px;
    border: none;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
}}
div.stButton button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
}}
.card {{
    padding: 24px;
    margin-bottom: 20px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.3s ease;
}}
.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.18);
}}
.card-arxiv {{
    background: linear-gradient(135deg, #ff9a8b, #ffeaa7, #fab1a0);
    border-left: 5px solid #e17055;
}}
.card-arxiv h3 {{
    color: #d63031;
    font-weight: 700;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}}
.card-wiki {{
    background: linear-gradient(135deg, #74b9ff, #0984e3, #a29bfe);
    border-left: 5px solid #6c5ce7;
}}
.card-wiki h3 {{
    color: #2d3436;
    font-weight: 700;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
}}
.card-duck {{
    background: linear-gradient(135deg, #fd79a8, #fdcb6e, #e84393);
    border-left: 5px solid #e84393;
}}
.card-duck h3 {{
    color: #2d3436;
    font-weight: 700;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
}}
@keyframes slideUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
</style>
""", unsafe_allow_html=True)

# ----------------- Heading -----------------
st.markdown("<h1>Smart AI-Based Search Engine Powered by Groq</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explore knowledge from Arxiv, Wikipedia, and the Web with AI-powered search!</p>", unsafe_allow_html=True)

# ----------------- Main App -----------------
if st.session_state.api_valid:
    st.sidebar.success("✅ Groq API Key Validated!")

    if st.sidebar.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your smart search assistant 🤖. Ask me anything!"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    from langchain.docstore.document import Document
    def extract_text(result):
        if isinstance(result, str):
            return result
        elif isinstance(result, Document):
            return result.page_content
        elif isinstance(result, list):
            return " ".join([extract_text(r) for r in result])
        return str(result)

    prompt = st.chat_input("💬 Type your question here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        tab1, tab2, tab3 = st.tabs(["📚 Arxiv", "🧠 Wikipedia", "🌐 DuckDuckGo"])

        # ----------------- Arxiv Tab -----------------
        with tab1:
            st.subheader("📚 Arxiv Answer")
            try:
                arxiv_result = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)).run(prompt)
                arxiv_content = extract_text(arxiv_result)
                answer_llm = ChatGroq(groq_api_key=api_key_input, model="llama-3.3-70b-versatile", streaming=True)
                answer_prompt = f"""
                User question: {prompt}
                Based on the following Arxiv paper content, provide a concise answer in numbered points,
                and also mention the title of the paper it came from.
                Paper content: {arxiv_content}
                """
                with st.chat_message("assistant"):
                    formatted_answer = answer_llm(answer_prompt).replace('\n','<br>')
                title = arxiv_content.split('Abstract:')[0].strip() if 'Abstract:' in arxiv_content else "Arxiv Paper"
                st.markdown(f"""
                <div class="card card-arxiv">
                    <h3>📚 {title}</h3>
                    <p>{formatted_answer}</p>
                    <a href="https://arxiv.org/search/?query={prompt.replace(' ','+')}" target="_blank">🔗 View Paper on Arxiv</a>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching Arxiv: {str(e)}")

        # ----------------- Wikipedia Tab -----------------
        with tab2:
            st.subheader("🧠 Wikipedia Answer")
            try:
                wiki_result = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)).run(prompt)
                wiki_content = extract_text(wiki_result)
                answer_llm = ChatGroq(groq_api_key=api_key_input, model="llama-3.3-70b-versatile", streaming=True)
                answer_prompt = f"""
                User question: {prompt}
                Based on the following Wikipedia content, provide a concise answer in numbered points.
                Content: {wiki_content}
                """
                with st.chat_message("assistant"):
                    formatted_answer = answer_llm(answer_prompt).replace('\n','<br>')
                st.markdown(f"""
                <div class="card card-wiki">
                    <h3>🧠 Wikipedia Summary</h3>
                    <p>{formatted_answer}</p>
                    <a href="https://en.wikipedia.org/wiki/{prompt.replace(' ','_')}" target="_blank">🔗 Read full article on Wikipedia</a>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching Wikipedia: {str(e)}")

        # ----------------- DuckDuckGo Tab -----------------
        with tab3:
            st.subheader("🌐 DuckDuckGo Answer")
            try:
                duck_result = DuckDuckGoSearchRun(name="Web Search").run(prompt)
                duck_content = extract_text(duck_result)
                answer_llm = ChatGroq(groq_api_key=api_key_input, model="llama-3.3-70b-versatile", streaming=True)
                answer_prompt = f"""
                User question: {prompt}
                Based on the following DuckDuckGo search results, provide a concise answer in numbered points.
                Results: {duck_content}
                """
                with st.chat_message("assistant"):
                    formatted_answer = answer_llm(answer_prompt).replace('\n','<br>')
                st.markdown(f"""
                <div class="card card-duck">
                    <h3>🌐 DuckDuckGo Results Summary</h3>
                    <p>{formatted_answer}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching DuckDuckGo: {str(e)}")

else:
    st.markdown("""
    <div style="text-align:center; margin-top:50px;">
        <h2 style="color:white;">🔒 Please enter a valid Groq API Key starting with <strong>gsk_</strong> to access the search engine.</h2>
    </div>
    """, unsafe_allow_html=True)

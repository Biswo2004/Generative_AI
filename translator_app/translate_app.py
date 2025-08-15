import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# 🎨 Streamlit Page Config
st.set_page_config(page_title="🌍 Groq LLM Translator", page_icon="🌐", layout="centered")

# 🌟 Sidebar for API Key Input
st.sidebar.header("🔑 API Key Setup")
st.sidebar.markdown("Enter your **Groq API Key** to enable translation.")

groq_api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="Paste your Groq API key here..."
)

if groq_api_key:
    st.session_state["GROQ_API_KEY"] = groq_api_key
    st.sidebar.success("✅ API Key saved!")
else:
    st.sidebar.warning("⚠️ Please enter your Groq API key.")

# 🧠 Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator that translates {source_lang} to {target_lang}."),
    ("user", "{text}")
])

# Only create model if API key is set
if "GROQ_API_KEY" in st.session_state and st.session_state["GROQ_API_KEY"]:
    model = ChatGroq(model="gemma2-9b-it", groq_api_key=st.session_state["GROQ_API_KEY"])
    parser = StrOutputParser()
    chain = prompt | model | parser

    # 🌍 App Title
    st.title("🌍 Groq LLM Translation Service")
    st.markdown(
        "<p style='text-align: center; color: grey;'>Translate text instantly using Groq's powerful LLM.</p>",
        unsafe_allow_html=True
    )

    # 📝 Input Section
    col1, col2 = st.columns(2)
    source_lang = col1.selectbox("Source Language", ["English", "French", "Spanish", "German", "Hindi", "Japanese", "Chinese"])
    target_lang = col2.selectbox("Target Language", ["English", "French", "Spanish", "German", "Hindi", "Japanese", "Chinese"])

    text = st.text_area("✏️ Enter text to translate", "", height=120, placeholder="Type your text here...")

    # 🚀 Translate button
    if st.button("🔄 Translate", type="primary"):
        if not text.strip():
            st.warning("⚠️ Please enter text to translate.")
        elif source_lang == target_lang:
            st.warning("⚠️ Source and target languages are the same.")
        else:
            try:
                with st.spinner("Translating... ⏳"):
                    result = chain.invoke({
                        "text": text,
                        "source_lang": source_lang,
                        "target_lang": target_lang
                    })
                st.success("✅ Translation Complete!")
                st.markdown(f"**Translation:**\n\n> {result}")
            except Exception as e:
                st.error(f"❌ An error occurred during translation: {str(e)}")

else:
    st.info("🔒 Please enter your Groq API key in the sidebar to start translating.")

# 📌 Footer with author credit
st.markdown(
    "<hr><p style='text-align: center; color: grey; font-size: 0.85em;'>"
    "Powered by Groq • Built with LangChain & Streamlit<br>"
    "Developed by <b>Biswojit</b>"
    "</p>",
    unsafe_allow_html=True
)

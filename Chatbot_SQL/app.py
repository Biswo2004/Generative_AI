import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler

##Set up the Streamlit app
st.set_page_config(page_title="MathsGPT:A complete solution of Mathematical problems and Data Research", page_icon=":guardsman:", layout="wide")
st.title("MathsGPT: A complete solution of Mathematical problems and Data Research")

groq_api_key = st.sidebar.text_input(label="Enter your Groq API Key", type="password", placeholder="Paste your Groq API key here...")

if not groq_api_key:
    st.info("Please add your Groq API key to continue.")
    st.stop()

llm = ChatGroq(model="gemma2-9b-it",api_key=groq_api_key)
wikipedia_wrapper = WikipediaAPIWrapper()

wikipedia_tool = Tool(
    name="Wikipedia",
    description="Useful for looking up information on Wikipedia.",
    func=wikipedia_wrapper.run,
    return_direct=True
)

## Intialize the Math tool
math_chain = LLMMathChain.from_llm(llm)
calculation_tool = Tool(
    name="Calculator",
    description="Useful for performing mathematical calculations.",
    func=math_chain.run,
    return_direct=True
)

prompt ="""You are a agent tasked for solving user's mathematical problems. Logically arrive at the solution using the tools available to you and display the final answer pointwise for each step for the question below.
Question:{question}
Answer: 
"""

prompt_template = PromptTemplate(
    template=prompt,
    input_variables=["question"]
)

## Combine all the tools into chain
chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)
reasoning_tool = Tool(
    name="Reasoning Chain",
    description="Useful for performing logical reasoning.",
    func=chain.run,
    return_direct=True
)

## Intialize the agents
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculation_tool, reasoning_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am MathsGPT, your assistant for mathematical problems and data research."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

## Function to generate the response
def generate_response(question):
    response = assistant_agent.invoke(
        {"input": question}
    )
    return response

## Lets start the interaction
question = st.text_area("Enter your question here:")

if st.button("Find my answer"):
    if question:
        with st.spinner("Generating response..."):
            response = generate_response(question)
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)
            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success("Response generated successfully!")
            st.write(response)
else:
    st.warning("Please enter a question to find an answer.")

import streamlit as st

from api import LLM
from executor import CodeExecutor


llm = LLM()
code_executor = CodeExecutor()


st.set_page_config(page_title="Tolvera LLM Chat")
st.title("💬 Chat with Tolvera-Integrated LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "code_block" not in st.session_state:
        st.session_state["code_block"] = None

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about Tolvera or generate code...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response_container = st.chat_message("assistant")
    response_text = response_container.empty()  
    streamed_response = ""

    with st.spinner("Generating response..."):
        for chunk in llm.generate_response(user_input):
            streamed_response += chunk
            response_text.markdown(streamed_response)

    st.session_state["messages"].append({"role": "assistant", "content": streamed_response})

    if "```python" in streamed_response:
        st.session_state["code_block"] = streamed_response.split("```python")[1].split("```")[0]

if st.session_state["code_block"]:

    if st.button("Run Code"):
        with st.spinner("Executing code..."):
            output = code_executor.save_and_execute(st.session_state["code_block"])
            st.text_area("Execution Output", output, height=200)

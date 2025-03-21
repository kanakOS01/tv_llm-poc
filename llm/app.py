import streamlit as st

# Streamlit UI Configuration
st.set_page_config(page_title="Tolvera LLM Chat")
st.title("💬 Chat with Tolvera-Integrated LLM")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
user_input = st.chat_input("Ask about Tolvera or generate code...")
if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call external function to get response (to be implemented in another module)
    from api import LLM  # Import from your backend logic
    llm = LLM()
    response = llm.generate_response(user_input)

    # Display LLM response
    st.chat_message("assistant").markdown(response)
    st.session_state["messages"].append({"role": "assistant", "content": response})

    # If response contains Python code, display it with a Run button
    if "```python" in response:
        code_block = response.split("```python")[1].split("```")[0]  # Extract code block
        st.code(code_block, language="python")

        # if st.button("Run Code"):
        #     from backend import execute_code  # Import execution function
        #     output = execute_code(code_block)
        #     st.text_area("Execution Output", output, height=200)

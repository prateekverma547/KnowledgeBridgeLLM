import streamlit as st
from dotenv import load_dotenv

from query import *
from query import QueryEngine

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

run_query = QueryEngine()


st.markdown(
    f"""
    ### ℹ️ Question & Answer BOT
    <span style="white-space: pre-line; font-family: Arial; font-size: 14px;">ARR Corp - SEC Report 2019 & 2020</span>
    """,
    unsafe_allow_html=True,
)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "You can ask me questions like:\n"}]

# Display messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# user input
if user_prompt := st.chat_input("Say Something"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = run_query.query_engine(user_prompt)

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

import os
import uuid
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/chatbot-rag-agent")

#  Create user_id automation
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer questions about Vietnamese history and culture.
        The agent uses retrieval-augment generation (RAG) over both
        structured and unstructured data related to Vietnam's past and cultural aspects.
        """
    )

    st.header("Example Questions")
    st.markdown("- What were the major dynasties that ruled Vietnam?")
    st.markdown("- What is the significance of the Hung Kings?")
    st.markdown("- How did French colonialism impact Vietnam?")
    st.markdown("- What was Ho Chi Minh's role in Vietnam's independence?")
    st.markdown("- What was the Battle of Dien Bien Phu about?")
    st.markdown("- What are some important traditional Vietnamese festivals?")
    st.markdown("- What are some key aspects of Vietnamese cuisine?")
    st.markdown("- How has Confucianism influenced Vietnamese society?")
    st.markdown("- What are some traditional Vietnamese art forms?")
    st.markdown("- How has Vietnam changed since Đổi Mới?")

st.title("Vietnamese History and Culture Chatbot")
st.info(
    "Ask me questions about Vietnamese dynasties, historical figures, cultural traditions, art, cuisine, and more!"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["output"])


if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {
        "user_id": st.session_state.user_id,
        "message": prompt
    }

    with st.spinner("Searching for an answer..."):
        try:
            response = requests.post(CHATBOT_URL, json=data)

            if response.status_code == 200:
                response_data = response.json()
                output_text = response_data.get("response", "No response provided.")
            else:
                output_text = (
                    "An error occurred while processing your message. "
                    "Please try again or rephrase your message."
                )

        except requests.exceptions.RequestException as e:
            output_text = f"An error occurred: {e}"

    # Hiển thị phản hồi từ bot
    st.chat_message("assistant").markdown(output_text)

    # Lưu phản hồi của bot vào lịch sử
    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
        }
    )

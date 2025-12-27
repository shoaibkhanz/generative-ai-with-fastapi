import requests
import streamlit as st

st.title("Fastapi chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    # response = requests.get(
    #     f"http://localhost:8000/generate/text", params={"prompt": prompt}
    # )
    response = requests.post(
        "http://localhost:8000/generate/text",
        json={"prompt": prompt, "model": "gpt-4o", "temperature": 0.5},
    )
    response.raise_for_status()

    with st.chat_message("assistant"):
        # st.markdown(response.text)
        st.markdown(response.json()["content"])

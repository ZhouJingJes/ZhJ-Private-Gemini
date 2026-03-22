import streamlit as st
import google.generativeai as genai

# 安全读取 API Key
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Gemini 私人助理", layout="centered")
st.title("🤖 Gemini 2.0 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 默认使用 2.0 Flash，额度高且速度快
    st.session_state.chat = genai.GenerativeModel('gemini-1.5-flash-8b').start_chat(history=[])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("说点什么..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
      

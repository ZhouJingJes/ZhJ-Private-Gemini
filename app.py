import streamlit as st
import google.generativeai as genai
import time
from google.api_core import exceptions

# 安全读取 API Key
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Gemini 私人助理", layout="centered")
st.title("🤖 我的私有 Gemini")

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 使用 1.5-flash-8b，稳定性最高
    st.session_state.chat = genai.GenerativeModel('gemini-1.5-flash').start_chat(history=[])

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入
if prompt := st.chat_input("说点什么..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # 尝试机制：如果报错，自动重试 3 次
        for attempt in range(3):
            try:
                response = st.session_state.chat.send_message(prompt)
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                break
            except exceptions.ResourceExhausted:
                if attempt < 2:
                    message_placeholder.markdown(f"⚠️ 服务器拥挤，正在第 {attempt+1} 次重试...")
                    time.sleep(2) # 等 2 秒再试
                else:
                    st.error("Google API 额度暂时耗尽，请 1 分钟后再试。")
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                break

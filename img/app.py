import time

import streamlit as st
from agent.react_agent import ReactAgent
from utils.history_handler import HistoryHandler

# 标题
st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

# 每个 Streamlit 会话创建一个独立的历史记录处理器
if "history_handler" not in st.session_state:
    st.session_state["history_handler"] = HistoryHandler()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))

        ai_response = response_messages[-1] if response_messages else ""
        st.session_state["message"].append({"role": "assistant", "content": ai_response})

        # 将本轮对话持久化到 data/history/
        st.session_state["history_handler"].save_turn(prompt, ai_response)

        st.rerun()

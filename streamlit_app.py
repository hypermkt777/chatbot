# streamlit_app.py

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

st.title("🏥 병원 예약 챗봇")

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 친절한 병원 예약 챗봇입니다. 환자의 질문에 병원 진료과, 진료시간, 위치, 예약 등 정보를 제공해주세요."}
    ]

# 사용자 입력 받기
user_input = st.text_input("👤 환자: ", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✅ 새로운 방식으로 GPT 호출
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )

    reply = chat_response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 대화 출력
for msg in st.session_state.messages[1:]:
    role = "🤖" if msg["role"] == "assistant" else "👤"
    st.markdown(f"{role} {msg['content']}")

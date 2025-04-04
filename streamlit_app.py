# streamlit_app.py

import streamlit as st
import openai

openai.api_key = "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"  # 보안상 실제로는 secrets.toml로 관리 권장

st.title("🏥 병원 예약 챗봇")

# 초기 세션 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 친절한 병원 예약 챗봇입니다. 환자의 질문에 병원 진료과, 진료시간, 위치, 예약 등 정보를 제공해주세요."}
    ]

# 사용자 입력
user_input = st.text_input("👤 환자: ", "")

if user_input:
    # 사용자 메시지 세션에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # GPT 응답
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )

    reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 채팅 기록 출력
for msg in st.session_state.messages[1:]:
    role = "🤖" if msg["role"] == "assistant" else "👤"
    st.markdown(f"{role} {msg['content']}")

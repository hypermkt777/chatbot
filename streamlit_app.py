# streamlit_app.py

import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
import json
import os
import pandas as pd

# ✅ OpenAI API 설정 (본인 API 키 입력)
client = OpenAI(api_key="ICT25_CLASS03_APIKEY
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")

# ✅ 페이지 설정
st.set_page_config(page_title="하이닥봇 - 병원 예약 챗봇", page_icon="🤖", layout="centered")

# ✅ 상단 로고 및 안내
st.markdown("""
<style>
.title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    color: #2C3E50;
    margin-bottom: 10px;
}
.sub {
    text-align: center;
    font-size: 17px;
    color: #7F8C8D;
}
.section {
    margin-top: 30px;
    padding: 20px;
    border-radius: 12px;
    background-color: #F9FAFB;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>

<div class="title">🤖 하이닥봇</div>
<div class="sub">병원 예약, 클릭 또는 말 한마디로 쉽게 완료하세요!</div>
""", unsafe_allow_html=True)

# ✅ 1. 자연어 기반 예약 요청
with st.expander("💬 자연어로 예약하기", expanded=False):
    user_query = st.chat_input("예: 내일 오후 3시에 치과 예약할래요")

    if user_query:
        with st.spinner("하이닥봇이 예약 내용을 파악하는 중입니다..."):
            gpt_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        사용자의 병원 예약 요청을 아래 JSON 형식으로 출력하세요.
                        {"진료과": "치과", "날짜": "2025-04-10", "시간": "오전 10시"}
                        날짜는 yyyy-mm-dd 형식, 시간은 "오전/오후 N시" 형식.
                        JSON만 출력하세요.
                        """
                    },
                    {"role": "user", "content": user_query}
                ]
            )
            raw_text = gpt_response.choices[0].message.content.strip()
            try:
                예약GPT = json.loads(raw_text)
                st.success("🎉 하이닥봇이 예약 정보를 분석했어요!")
                st.json(예약GPT)
            except:
                st.warning("정확히 인식하지 못했어요. 다시 말씀해주세요.")
                예약GPT = {}
else:
    예약GPT = {}

# ✅ 2. 클릭 기반 예약 입력
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 📝 클릭해서 예약하기")

진료과목 = ["치과", "피부과", "내과", "정형외과", "소아과"]
진료과 = st.radio("1️⃣ 진료과 선택", 진료과목,
                  index=진료과목.index(예약GPT["진료과"]) if 예약GPT.get("진료과") in 진료과목 else 0)

오늘 = datetime.today()
날짜옵션 = [(오늘 + timedelta(days=i)).strftime("%Y-%m-%d (%a)") for i in range(7)]
날짜str = 예약GPT.get("날짜")
예약날짜 = st.selectbox("2️⃣ 예약 날짜 선택", 날짜옵션,
    index=날짜옵션.index(datetime.strptime(날짜str, "%Y-%m-%d").strftime("%Y-%m-%d (%a)")) if 날짜str else 0)

시간옵션 = ["오전 9시", "오전 10시", "오전 11시", "오후 2시", "오후 3시", "오후 4시", "오후 5시"]
시간str = 예약GPT.get("시간")
예약시간 = st.radio("3️⃣ 예약 시간 선택", 시간옵션,
                    index=시간옵션.index(시간str) if 시간str in 시간옵션 else 0,
                    horizontal=True)

col1, col2 = st.columns(2)
with col1:
    성함 = st.text_input("👤 예약자 성함")
with col2:
    연락처 = st.text_input("📱 연락처 (예: 010-1234-5678)")

st.markdown('</div>', unsafe_allow_html=True)

# ✅ 3. 예약 처리 및 CSV 저장
if st.button("✅ 하이닥봇에게 예약 맡기기", use_container_width=True):
    if not 성함 or not 연락처:
        st.warning("이름과 연락처를 입력해 주세요 🙏")
    else:
        st.success("🎉 예약이 완료되었습니다!")
        st.markdown("---")
        st.markdown(f"""
        ### 🧾 예약 확인서

        - **진료과**: `{진료과}`  
        - **예약 날짜**: `{예약날짜}`  
        - **예약 시간**: `{예약시간}`  
        - **이름**: `{성함}`  
        - **연락처**: `{연락처}`
        """)

        예약정보 = {
            "예약일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "진료과": 진료과,
            "예약날짜": 예약날짜,
            "예약시간": 예약시간,
            "성함": 성함,
            "연락처": 연락처
        }

        # CSV 저장
        csv_file = "예약내역.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([예약정보])], ignore_index=True)
        else:
            df = pd.DataFrame([예약정보])
        df.to_csv(csv_file, index=False)
        st.info("📦 예약 내역이 저장되었습니다.")

# ✅ 4. 관리자 전용 예약 목록 보기
st.markdown("---")
st.markdown("### 🔐 하이닥봇 관리자 모드")

admin_pw = st.text_input("관리자 비밀번호", type="password", placeholder="비밀번호를 입력하세요")

if admin_pw == "0070":  # 👉 비밀번호는 필요시 변경 가능
    st.success("✅ 관리자 인증 완료!")
    csv_file = "예약내역.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        st.markdown("#### 📋 현재까지 예약된 목록")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 예약된 내역이 없습니다.")
elif admin_pw and admin_pw != "hidocadmin":
    st.error("❌ 비밀번호가 올바르지 않습니다.")

# streamlit_app.py

import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="병원 예약 챗봇", page_icon="🩺", layout="centered")

# 상단 헤더
st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    color: #2C3E50;
    margin-bottom: 10px;
}
.sub {
    text-align: center;
    font-size: 16px;
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

<div class="title">🏥 병원 예약 챗봇</div>
<div class="sub">클릭 몇 번으로 빠르고 쉽게 예약해보세요 :)</div>
""", unsafe_allow_html=True)

# ✅ 진료 예약 폼 UI
st.markdown('<div class="section">', unsafe_allow_html=True)

st.markdown("### 1️⃣ 진료과를 선택해주세요")
진료과 = st.radio("", ["치과", "피부과", "내과", "정형외과", "소아과"], index=0)

st.markdown("### 2️⃣ 예약 날짜를 선택해주세요")
오늘 = datetime.today()
날짜옵션 = [(오늘 + timedelta(days=i)).strftime("%Y-%m-%d (%a)") for i in range(7)]
예약날짜 = st.selectbox("", 날짜옵션)

st.markdown("### 3️⃣ 시간대를 선택해주세요")
시간옵션 = ["오전 9시", "오전 10시", "오전 11시", "오후 2시", "오후 3시", "오후 4시", "오후 5시"]
예약시간 = st.radio("", 시간옵션, horizontal=True)

st.markdown("### 4️⃣ 예약자 정보를 입력해주세요")
col1, col2 = st.columns(2)
with col1:
    성함 = st.text_input("👤 성함")
with col2:
    연락처 = st.text_input("📱 연락처")

st.markdown("</div>", unsafe_allow_html=True)

# ✅ 예약 버튼 및 결과 출력
if st.button("✅ 예약하기", use_container_width=True):
    if not 성함 or not 연락처:
        st.warning("이름과 연락처를 입력해주세요 🙏")
    else:
        st.success("🎉 예약이 완료되었습니다! 아래 정보를 확인해주세요.")
        st.markdown("---")
        st.markdown(f"""
        ### 🧾 예약 확인서

        - **진료과**: `{진료과}`  
        - **예약일**: `{예약날짜}`  
        - **예약시간**: `{예약시간}`  
        - **성함**: `{성함}`  
        - **연락처**: `{연락처}`  
        
        병원 방문 전날, 알림톡으로 예약 내용을 다시 안내드릴게요 😊
        """)

        # 예약 데이터 구조
        예약정보 = {
            "진료과": 진료과,
            "예약날짜": 예약날짜,
            "예약시간": 예약시간,
            "성함": 성함,
            "연락처": 연락처
        }

        # 추후: st.json(예약정보) 또는 파일 저장 가능

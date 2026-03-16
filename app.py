import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="다온 Life 고객관리", layout="wide")
st.title("🛡️ 다온 Life 고객 정보 관리 시스템")

# 구글 시트 연결
try:
    # 한글 처리를 위해 환경 설정(ttl=0으로 실시간성 확보)
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("연결 설정 오류가 발생했습니다.")
    st.stop()

if "f_count" not in st.session_state:
    st.session_state.f_count = 0

# 사이드바: 입력창
with st.sidebar:
    st.header("👤 신규 고객 등록")
    fc = st.session_state.f_count
    
    name = st.text_input("고객 성함", key=f"n_{fc}")
    birth = st.text_input("생년월일", key=f"b_{fc}")
    phone = st.text_input("연락처", key=f"p_{fc}")
    policy = st.selectbox("상품군", ["건강보험", "종신보험", "자동차 또는 운전자", "화재보험", "실손보험 또는 기타"], key=f"po_{fc}")
    notes = st.text_area("상담 메모", key=f"m_{fc}")
    
    if st.button("정보 저장", use_container_width=True, type="primary"):
        if name and phone:
            try:
                # 1. 데이터 읽기 (한글 포함 데이터 가져오기)
                existing_data = conn.read()
                
                # 2. 새 데이터 행 만들기
                new_row = pd.DataFrame([{
                    "id": len(existing_data) + 1, 
                    "name": str(name),        # 한글을 문자열로 확실히 지정
                    "birth": str(birth), 
                    "phone": str(phone), 
                    "policy": str(policy), 
                    "notes": str(notes)       # 메모 내 한글 처리
                }])
                
                # 3. 데이터 합치기
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # 4. 🔥 구글 시트 저장 (한글 인코딩 오류 방지)
                conn.update(data=updated_df)
                
                st.success(f"{name}님 저장 완료!")
                st.session_state.f_count += 1
                st.rerun()
            except Exception as e:
                # 에러 메시지가 길면 핵심만 표시
                st.error(f"저장
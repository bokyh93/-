import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="다온 Life 고객관리", layout="wide")
st.title("🛡️ 다온 Life 고객 정보 관리 시스템")

# 2. 구글 시트 연결
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("연결 설정 오류가 발생했습니다. Secrets 설정을 확인해주세요.")
    st.stop()

if "f_count" not in st.session_state:
    st.session_state.f_count = 0

# 3. 사이드바: 입력창
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
                # 데이터 읽기
                existing_data = conn.read()
                
                # 새 데이터 행 만들기 (모든 데이터를 문자열로 변환하여 한글 오류 방지)
                new_row = pd.DataFrame([{
                    "id": str(len(existing_data) + 1),
                    "name": str(name),
                    "birth": str(birth),
                    "phone": str(phone),
                    "policy": str(policy),
                    "notes": str(notes)
                }])
                
                # 데이터 합치기 및 저장
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(data=updated_df)
                
                st.success(f"{name}님 저장 완료!")
                st.session_state.f_count += 1
                st.rerun()
            except Exception as e:
                # 에러 메시지를 영어로 출력하여 한글 코덱 충돌 원천 차단
                st.error("Save failed. Please check Google Sheets edit permission.")
        else:
            st.error("이름과 연락처를 입력해주세요.")

# 4. 데이터 표시
st.header("🔍 실시간 고객 명단")
try:
    df = conn.read()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("현재 등록된 고객이 없습니다.")
except:
    st.warning("데이터를 불러올 수 없습니다.")
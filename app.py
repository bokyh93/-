import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# [필수] 페이지 설정
st.set_page_config(page_title="다온 Life 고객관리", layout="wide")
st.title("🛡️ 다온 Life 고객 정보 관리 시스템")

# --- 핵심: 여기서 'conn'을 정의합니다 ---
# 만약 Secrets 설정이 안 되어 있으면 여기서 에러가 날 수 있습니다.
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("구글 시트 연결 설정(conn)에 실패했습니다. Secrets를 확인해주세요.")
    st.stop()
# ---------------------------------------

# 초기화 세션 관리
if "f_count" not in st.session_state:
    st.session_state.f_count = 0

# 사이드바: 입력창
with st.sidebar:
    st.header("👤 신규 고객 등록")
    fc = st.session_state.f_count
    
    name = st.text_input("고객 성함", key=f"n_{fc}")
    birth = st.text_input("생년월일", key=f"b_{fc}")
    phone = st.text_input("연락처", key=f"p_{fc}")
    policy = st.selectbox("상품군", ["건강보험", "종신보험", "자동차 또는 운전자", "화재보험", "실손보험 및 기타"], key=f"po_{fc}")
    notes = st.text_area("상담 메모", key=f"m_{fc}")
    
    if st.button("정보 저장", use_container_width=True, type="primary"):
        if name and phone:
            try:
                # 1. 데이터 읽기 (정의된 'conn' 사용)
                existing_data = conn.read()
                
                # 2. 새 데이터 만들기
                new_row = pd.DataFrame([{
                    "id": len(existing_data) + 1, "name": name, "birth": birth, 
                    "phone": phone, "policy": policy, "notes": notes
                }])
                
                # 3. 데이터 합치기
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # 4. 구글 시트 저장 (정의된 'conn' 사용)
                conn.update(data=updated_df)
                
                st.success(f"{name}님 저장 완료!")
                st.session_state.f_count += 1
                st.rerun()
            except Exception as e:
                st.error(f"데이터 처리 중 오류 발생: {e}")
        else:
            st.error("이름과 연락처를 입력해주세요.")

# 메인 화면: 데이터 표시
st.header("🔍 실시간 고객 명단")
try:
    # 정의된 'conn'을 사용하여 데이터 표시
    df = conn.read()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("시트에 표시할 데이터가 없습니다.")
except Exception as e:
    st.warning("시트 데이터를 불러올 수 없습니다. 공유 설정을 확인하세요.")
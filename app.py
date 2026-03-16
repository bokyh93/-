import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="다온 Life 고객관리", layout="wide")
st.title("🛡️ 다온 Life 고객 정보 관리 시스템")

# 2. 구글 시트 연결 도구 정의 (중요: 여기서 'conn'을 만듭니다)
conn = st.connection("gsheets", type=GSheetsConnection)

# 초기화 세션 관리
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
    
    col1, col2 = st.columns(2)
    with col1:
        # [정보 저장] 버튼 클릭 시 로직
        if st.button("정보 저장", use_container_width=True, type="primary"):
            if name and phone:
                try:
                    # ① 기존 데이터 읽어오기
                    existing_data = conn.read()
                    
                    # ② 새 데이터 행 만들기
                    new_row = pd.DataFrame([{
                        "id": len(existing_data) + 1,
                        "name": name,
                        "birth": birth,
                        "phone": phone,
                        "policy": policy,
                        "notes": notes
                    }])
                    
                    # ③ 기존 데이터와 합치기
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    
                    # ④ 구글 시트에 실제로 쓰기 (저장)
                    conn.update(data=updated_df)
                    
                    st.success(f"{name}님 정보가 구글 시트에 저장되었습니다!")
                    st.session_state.f_count += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"저장 실패! 공유 권한을 확인하세요.")
                    # Manage App 로그에서 상세 에러를 볼 수 있습니다.
            else:
                st.error("이름과 연락처를 입력해주세요.")
                
    with col2:
        if st.button("내용 초기화", use_container_width=True):
            st.session_state.f_count += 1
            st.rerun()

# 4. 메인 화면: 데이터 표시
st.header("🔍 실시간 고객 명단 (Google Sheets)")

# 실시간으로 시트 내용을 읽어와서 보여줍니다
try:
    df = conn.read()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("시트에 데이터가 없습니다.")
except:
    st.warning("구글 시트 연결 설정을 확인해주세요 (Secrets 설정 필요)")
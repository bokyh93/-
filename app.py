import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="고객관리 시스템", layout="wide")
st.title("🛡️ 보험대리점 고객 정보 관리 시스템")

# 2. 구글 시트 ID 설정
SHEET_ID = "여기에_구글시트_ID를_넣으세요"
SHEET_NAME = "Sheet1" 
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# 세션 상태 초기화 (데이터를 임시 보관할 저장소)
if "temp_data" not in st.session_state:
    st.session_state.temp_data = pd.DataFrame()
if "f_count" not in st.session_state:
    st.session_state.f_count = 0

def load_data():
    try:
        # 구글 시트에서 데이터 가져오기
        df = pd.read_csv(URL, encoding='utf-8')
        return df
    except:
        return pd.DataFrame(columns=["id", "name", "birth", "phone", "policy", "notes"])

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
       if st.button("정보 저장", use_container_width=True, type="primary"):
        if name and phone:
            # 1. 구글 시트에서 기존 데이터 불러오기
            existing_data = conn.read()
            
            # 2. 새 데이터 행 만들기
            new_row = pd.DataFrame([{
                "id": len(existing_data) + 1,
                "name": name,
                "birth": birth,
                "phone": phone,
                "policy": policy,
                "notes": notes
            }])
            
            # 3. 기존 데이터와 새 데이터 합치기
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            
            # 4. 🔥 실제 구글 시트에 업데이트 (핵심!)
            try:
                conn.update(data=updated_df)
                st.success(f"{name}님 정보가 구글 시트에 안전하게 저장되었습니다!")
                
                # 저장 성공 후 입력창 초기화
                st.session_state.f_count += 1
                st.rerun()
            except Exception as e:
                st.error(f"저장 중 오류가 발생했습니다: {e}")
                st.info("구글 시트의 공유 설정이 '편집자'로 되어있는지 확인해주세요.")
        else:
            st.error("이름과 연락처를 입력해주세요.")
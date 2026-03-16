import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="다온 Life", layout="wide")
st.title("🛡️ 다온 Life 고객관리 시스템 (최종 연결 모드)")

# 1. 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 사이드바 입력창
with st.sidebar:
    st.header("👤 정보 입력")
    name = st.text_input("고객 성함")
    phone = st.text_input("연락처")
    
    if st.button("💾 정보 저장 (강제 전송)", type="primary"):
        if name and phone:
            try:
                # [단계 1] 기존 데이터 가져오기
                df = conn.read()
                
                # [단계 2] 새 데이터 생성
                new_data = pd.DataFrame([{"name": name, "phone": phone}])
                
                # [단계 3] 데이터 합치기
                updated_df = pd.concat([df, new_data], ignore_index=True)
                
                # [단계 4] 구글 시트에 업데이트
                # (가장 단순한 호출 방식으로 변경)
                conn.update(data=updated_df)
                
                st.success(f"✅ {name}님 저장 성공!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 저장 실패 원인: {e}")
        else:
            st.warning("이름과 번호를 입력하세요.")

# 3. 데이터 표시
st.header("🔍 저장된 명단")
try:
    display_df = conn.read()
    st.dataframe(display_df, use_container_width=True)
except:
    st.info("데이터를 불러올 수 없습니다.")
# home.py
import streamlit as st
from db import get_all_events, delete_all_events
import datetime

def main():
    st.title("프로젝트 일정 관리")
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📊 현황", "⚙️ 관리"])
    
    with tab1:
        # 데이터 통계
        events_df = get_all_events()
        if not events_df.empty:
            st.subheader("📈 일정 통계")
            st.metric("전체 일정 수", len(events_df))
        else:
            st.info("등록된 일정이 없습니다.")
    
    with tab2:
        st.subheader("⚠️ 데이터 관리")
        
        # 경고 메시지
        st.warning("""
        주의사항
        - 이 작업은 되돌릴 수 없습니다!
        - 모든 일정 데이터가 영구적으로 삭제됩니다.
        - 삭제 전 필요한 데이터는 백업해주세요.
        """)
        
        # 삭제 코드 입력과 버튼을 나란히 배치
        col1, col2 = st.columns([2,1])
        
        with col1:
            delete_code = st.text_input(
                "데이터 삭제 코드", 
                type="password",
                label_visibility="collapsed",
                placeholder="삭제 코드 입력"
            )
        
        with col2:
            if st.button("전체 데이터 삭제", type="primary"):
                if delete_code == "1035":
                    try:
                        delete_all_events()
                        st.success("✅ 모든 데이터가 삭제되었습니다!")
                        st.balloons()
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"오류 발생: {str(e)}")
                else:
                    st.error("올바른 코드를 입력해주세요.")

if __name__ == "__main__":
    main()
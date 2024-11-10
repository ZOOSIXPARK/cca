# pages/3_csv_import.py
import streamlit as st
import pandas as pd
from db import add_event
import io

# 색상 정의
COLOR_MAPPING = {
    "빨간색": "#FF6B6B",
    "파란색": "#45B7D1",
    "초록색": "#4ECDC4",
    "보라색": "#845EC2",
    "주황색": "#FF9671"
}

def main():
    st.title("📤 CSV 일정 업로드")
    
    # CSV 파일 형식 안내
    st.info("""
    CSV 파일 형식 안내:
    - 필수 컬럼: title(일정제목), start_date(시작일), end_date(종료일)
    - 선택 컬럼: color(색상), description(설명)
    - 날짜 형식: YYYY-MM-DD (예: 2024-11-10)
    - 색상 입력: 빨간색, 파란색, 초록색, 보라색, 주황색 중 선택
    """)
    
    # 색상 견본 표시
    
    # 샘플 CSV 다운로드 기능
    sample_data = {
        'title': ['프로젝트 시작', '중간 발표', '최종 발표'],
        'start_date': ['2024-11-10', '2024-11-15', '2024-11-20'],
        'end_date': ['2024-11-10', '2024-11-15', '2024-11-20'],
        'color': ['빨간색', '파란색', '초록색'],  # 한글 색상명 사용
        'description': ['프로젝트 킥오프', '중간 진행상황 보고', '최종 결과 발표']
    }
    sample_df = pd.DataFrame(sample_data)
    
    sample_csv = sample_df.to_csv(index=False)
    st.download_button(
        label="📥 샘플 CSV 다운로드",
        data=sample_csv,
        file_name="sample_events.csv",
        mime="text/csv"
    )
    
    # CSV 파일 업로드
    uploaded_file = st.file_uploader("CSV 파일 선택", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # 필수 컬럼 확인
            required_columns = ['title', 'start_date', 'end_date']
            if not all(col in df.columns for col in required_columns):
                st.error("필수 컬럼이 없습니다. title, start_date, end_date 컬럼이 필요합니다.")
                return
            
            # 색상 변환
            if 'color' in df.columns:
                # 색상명이 매핑에 없는 경우 기본 색상(빨간색) 사용
                df['color'] = df['color'].apply(lambda x: COLOR_MAPPING.get(x, COLOR_MAPPING['빨간색']))
            else:
                df['color'] = COLOR_MAPPING['빨간색']
            
            # 데이터 미리보기
            st.subheader("데이터 미리보기")
            preview_df = df.copy()
            if 'color' in preview_df.columns:
                # 미리보기에서는 다시 색상 이름으로 변환
                reverse_color_mapping = {v: k for k, v in COLOR_MAPPING.items()}
                preview_df['color'] = preview_df['color'].map(reverse_color_mapping)
            st.dataframe(preview_df)
            
            # 업로드 확인
            if st.button("일정 등록하기"):
                success_count = 0
                for _, row in df.iterrows():
                    try:
                        add_event(
                            title=row['title'],
                            start_date=row['start_date'],
                            end_date=row['end_date'],
                            color=row['color'],
                            description=row.get('description', '')
                        )
                        success_count += 1
                    except Exception as e:
                        st.error(f"일정 '{row['title']}' 등록 실패: {str(e)}")
                
                st.success(f"총 {success_count}개의 일정이 등록되었습니다.")
                
        except Exception as e:
            st.error(f"CSV 파일 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
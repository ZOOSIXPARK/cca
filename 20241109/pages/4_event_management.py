# pages/4_event_management.py
import streamlit as st
import pandas as pd
from db import get_all_events, delete_all_events
import sqlite3
from datetime import datetime
import calendar
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time 


COLOR_MAPPING = {
    "#FF6B6B": "빨간색",
    "#45B7D1": "파란색",
    "#4ECDC4": "초록색",
    "#845EC2": "보라색",
    "#FF9671": "주황색"
}

def convert_color_to_name(color_code):
    return COLOR_MAPPING.get(color_code, "빨간색")  # 기본값은 빨간색


def create_calendar_image(events_df, year, month):
    # 달력 데이터 준비
    cal = calendar.monthcalendar(year, month)
    
    # Plotly figure 생성
    fig = go.Figure()
    
    # 테이블 데이터 준비
    table_data = []
    colors = []
    
    # 요일 헤더
    weekdays = ['일', '월', '화', '수', '목', '금', '토']
    table_data.append(weekdays)
    colors.append(['rgb(255,0,0)' if d == '일' else 'rgb(0,0,255)' if d == '토' else 'black' for d in weekdays])
    
    # 달력 데이터와 이벤트 매핑
    for week in cal:
        week_data = []
        week_colors = []
        for i, day in enumerate(week):
            if day == 0:
                cell_content = ""
                cell_color = 'white'
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                day_events = events_df[
                    (pd.to_datetime(events_df['start_date']) <= date_str) &
                    (pd.to_datetime(events_df['end_date']) >= date_str)
                ]
                
                # 날짜와 이벤트 텍스트 결합
                cell_content = f"{day}\n"
                if not day_events.empty:
                    events_text = "\n".join([f"• {row['title']}" for _, row in day_events.iterrows()])
                    cell_content += events_text
                
                # 주말 색상 설정
                cell_color = 'rgb(255,0,0)' if i == 0 else 'rgb(0,0,255)' if i == 6 else 'black'
            
            week_data.append(cell_content)
            week_colors.append(cell_color)
        
        table_data.append(week_data)
        colors.append(week_colors)
    
    # Plotly 테이블 생성
    fig.add_trace(
        go.Table(
            header=dict(
                values=[f'<b>{day}</b>' for day in weekdays],
                line_color='white',
                fill_color='lightgrey',
                align='center',
                font=dict(size=14, color=colors[0])
            ),
            cells=dict(
                values=[[row[i] for row in table_data[1:]] for i in range(7)],
                line_color='white',
                fill_color='white',
                align='center',
                height=80,
                font=dict(size=12),
                font_color=[[colors[i+1][j] for i in range(len(table_data)-1)] for j in range(7)]
            )
        )
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title=dict(
            text=f'{year}년 {month}월',
            x=0.5,
            font=dict(size=24)
        ),
        width=800,
        height=600,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def main():
    st.title("📋 일정 관리")
    
    # 데이터 가져오기
    events_df = get_all_events()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📋 전체 조회","🔍고급검색", "📥 다운로드"])
    
    with tab1:
        st.subheader("전체 일정 목록")
        if not events_df.empty:
            # 날짜순으로 정렬
            events_df_sorted = events_df.sort_values('start_date', ascending=False)
            
            # 데이터프레임 표시
            st.dataframe(
                events_df_sorted[['title', 'start_date', 'end_date', 'description']],
                column_config={
                    'title': '일정 제목',
                    'start_date': '시작일',
                    'end_date': '종료일',
                    'description': '설명'
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("등록된 일정이 없습니다.")
    with tab2:
        st.subheader("고급 조회")
        
        # 검색 조건 설정
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "시작일",
                value=datetime.strptime(events_df['start_date'].min(), '%Y-%m-%d') if not events_df.empty else datetime.now(),
                key="search_start_date"
            )
        
        with col2:
            end_date = st.date_input(
                "종료일",
                value=datetime.strptime(events_df['end_date'].max(), '%Y-%m-%d') if not events_df.empty else datetime.now(),
                key="search_end_date"
            )
        
        # 키워드 검색
        keyword = st.text_input("검색어 (제목 또는 설명에 포함)", placeholder="검색어 입력")
        
        # 추가 필터 옵션
        with st.expander("추가 검색 옵션"):
            col1, col2 = st.columns(2)
            with col1:
                sort_by = st.selectbox(
                    "정렬 기준",
                    options=["시작일", "종료일", "제목"],
                    format_func=lambda x: {
                        "시작일": "시작일",
                        "종료일": "종료일",
                        "제목": "제목"
                    }[x]
                )
            
            with col2:
                sort_order = st.selectbox(
                    "정렬 순서",
                    options=["오름차순", "내림차순"]
                )
        
        # 검색 실행
        if not events_df.empty:
            # 날짜 필터링
            mask = pd.to_datetime(events_df['start_date']) >= pd.to_datetime(start_date)
            mask &= pd.to_datetime(events_df['end_date']) <= pd.to_datetime(end_date)
            
            # 키워드 필터링
            if keyword:
                keyword_lower = keyword.lower()
                mask &= (
                    events_df['title'].str.lower().str.contains(keyword_lower, na=False) |
                    events_df['description'].str.lower().str.contains(keyword_lower, na=False)
                )
            
            filtered_df = events_df[mask]
            
            # 정렬
            sort_column = {
                "시작일": "start_date",
                "종료일": "end_date",
                "제목": "title"
            }[sort_by]
            
            filtered_df = filtered_df.sort_values(
                sort_column,
                ascending=(sort_order == "오름차순")
            )
            
            # 결과 표시
            st.subheader(f"검색 결과 ({len(filtered_df)}건)")
            
            if not filtered_df.empty:
                # 검색 결과 테이블
                st.dataframe(
                    filtered_df[['title', 'start_date', 'end_date', 'description']],
                    column_config={
                        'title': '일정 제목',
                        'start_date': '시작일',
                        'end_date': '종료일',
                        'description': '설명'
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("검색 조건에 맞는 일정이 없습니다.")
        else:
            st.info("등록된 일정이 없습니다.")

    
    with tab3:
        st.subheader("데이터 다운로드")
        
        if not events_df.empty:
            # 데이터프레임에 색상 이름 컬럼 추가
            export_df = events_df.copy()
            export_df['color'] = export_df['color'].apply(convert_color_to_name)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 엑셀 다운로드
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    # export_df의 컬럼 순서와 이름을 원하는 형식으로 변경
                    export_df = export_df[['title', 'start_date', 'end_date', 'color', 'description']]
                    export_df.columns = ['title', 'start_date', 'end_date', 'color', 'description']
                    export_df.to_excel(
                        writer, 
                        index=False, 
                        sheet_name='Events'
                    )
                
                st.download_button(
                    label="📥 엑셀 다운로드",
                    data=excel_buffer.getvalue(),
                    file_name="events.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # CSV 다운로드
                csv_buffer = io.StringIO()
                export_df.to_csv(
                    csv_buffer, 
                    index=False, 
                    encoding='utf-8-sig'
                )
                
                st.download_button(
                    label="📥 CSV 다운로드",
                    data=csv_buffer.getvalue().encode('utf-8-sig'),
                    file_name="events.csv",
                    mime="text/csv"
                )
        
        st.divider()
        
        st.subheader("캘린더 확인")
        # 년/월 선택
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("년도", 
                              range(2020, 2031),
                              index=datetime.now().year - 2020)
        with col2:
            month = st.selectbox("월",
                               range(1, 13),
                               index=datetime.now().month - 1)
        
        if not events_df.empty:
            # 캘린더 생성 및 표시
            fig = create_calendar_image(events_df, year, month)
            st.plotly_chart(fig, use_container_width=True)
            
            # 이미지 다운로드 버튼
            img_bytes = fig.to_image(format="png", width=800, height=600, scale=2)
            st.download_button(
                label="📥 캘린더 이미지 다운로드",
                data=img_bytes,
                file_name=f"calendar_{year}_{month:02d}.png",
                mime="image/png"
            )
        else:
            st.info("표시할 일정이 없습니다.")

if __name__ == "__main__":
    main()
# pages/2_gantt.py
import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import sqlite3

def get_all_events():
    conn = sqlite3.connect('calendar.db')
    # SQL 쿼리 결과를 직접 DataFrame으로 변환
    df = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return df

def main():
    st.title('📊 Gantt Chart')

    # DB에서 이벤트 가져오기
    events_df = get_all_events()

    if len(events_df) > 0:  # DataFrame이 비어있지 않은지 확인
        # 간트 차트용 데이터 준비
        gantt_data = []
        for _, row in events_df.iterrows():
            gantt_data.append(dict(
                Task=row['title'],
                Start=pd.to_datetime(row['start_date']),
                Finish=pd.to_datetime(row['end_date']),
                Description=row['description'],
                Resource=row['title']
            ))
        
        # 간트 차트 생성
        fig = ff.create_gantt(
            gantt_data,
            colors={row['title']: row['color'] for _, row in events_df.iterrows()},
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True
        )
        
        # 차트 레이아웃 설정
        fig.update_layout(
            title='Project Schedule',
            xaxis_title='Date',
            height=400 + (len(events_df) * 40),
            font=dict(size=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 일정 목록 표시
        st.subheader("일정 목록")
        st.dataframe(
            events_df[['title', 'start_date', 'end_date', 'description']],
            column_config={
                'title': '일정 제목',
                'start_date': '시작일',
                'end_date': '종료일',
                'description': '설명'
            }
        )
    else:
        st.info("등록된 일정이 없습니다. 캘린더 페이지에서 일정을 추가해주세요.")

if __name__ == "__main__":
    main()
# pages/1_calendar.py
import streamlit as st
from streamlit_calendar import calendar
import datetime
import sqlite3
import pandas as pd

# 색상 정의
COLOR_MAPPING = {
    "빨간색": "#FF6B6B",
    "파란색": "#45B7D1",
    "초록색": "#4ECDC4",
    "보라색": "#845EC2",
    "주황색": "#FF9671"
}

# DB 연결 함수
def init_db():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         start_date DATE NOT NULL,
         end_date DATE NOT NULL,
         color TEXT,
         description TEXT)
    ''')
    conn.commit()
    conn.close()

def add_event(title, start_date, end_date, color, description=""):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (title, start_date, end_date, color, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, start_date, end_date, color, description))
    conn.commit()
    conn.close()

def get_all_events():
    conn = sqlite3.connect('calendar.db')
    events = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return events

# 메인 앱
st.title('📅 캘린더')


# DB 초기화
init_db()

# DB에서 이벤트 가져오기
events_df = get_all_events()
events = []
for _, row in events_df.iterrows():
    events.append({
        'title': row['title'],
        'start': row['start_date'],
        'end': row['end_date'],
        'backgroundColor': row['color']
    })

# 캘린더 옵션
calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth",
    "selectable": True,
    "editable": True,
    "locale": "ko",
    "height": 650,
    
    # 전체적인 테마 색상
    "themeSystem": "standard",
    
    # 헤더 스타일링
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    
    # 버튼 스타일링
    "buttonText": {
        "today": "오늘",
        "month": "월",
        "week": "주",
        "day": "일"
    },
    
    # 일반 날짜 셀 스타일링
    "dayCellClassNames": "custom-day",
    
    # 이벤트 관련 스타일링
    "eventDisplay": "block",
    "eventTimeFormat": {
        "hour": "2-digit",
        "minute": "2-digit",
        "meridiem": False
    },
    "eventBackgroundColor": "#94A684",  # 기본 이벤트 배경색
    "eventBorderColor": "rgba(255,255,255,0.2)",
    "eventTextColor": "#FFFFFF",
    
    # 테이블 스타일링
    "slotLabelFormat": {
        "hour": "2-digit",
        "minute": "2-digit",
        "hour12": False
    },
    
    # 선택 관련 스타일링
    "selectable": True,
    "selectMirror": True,
    "selectMinDistance": 0,
    
    # 날짜 헤더 포맷
    "dayHeaderFormat": { "weekday": "short" },
    
    # 추가 스타일 커스텀
    "bootstrapFontAwesome": {
        "prev": "chevron-left",
        "next": "chevron-right"
    },
    
    # CSS 커스텀
    "contentHeight": "auto",
    "aspectRatio": 1.8,
    
    # 날짜 클릭 하이라이트 색상
    "nowIndicator": True,
    "now": datetime.datetime.now().strftime("%Y-%m-%d"),
    
    # 추가 스타일링
    "viewClassNames": "custom-view",
    "dayMaxEvents": True,
    "firstDay": 0,  # 일요일부터 시작
    
    # 헤더 날짜 포맷
    "titleFormat": {
        "year": "numeric",
        "month": "long"
    },
}

# 캘린더 스타일링을 위한 CSS 추가
st.markdown("""
<style>
/* 캘린더 헤더 스타일 */
.fc-header-toolbar {
    padding: 10px 0;
    background-color: #ffffff;
    border-radius: 8px;
    margin-bottom: 15px !important;
}

/* 버튼 스타일링 */
.fc-button {
    background-color: #756AB6 !important;
    border: none !important;
    color: white !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

.fc-button:hover {
    background-color: #8b81c9 !important;
}

/* 오늘 버튼 특별 스타일 */
.fc-today-button {
    background-color: #94A684 !important;
}

/* 제목 스타일링 */
.fc-toolbar-title {
    color: #333333 !important;
    font-size: 1.5em !important;
    font-weight: 600 !important;
}

/* 요일 헤더 스타일링 */
.fc-col-header-cell {
    background-color: #f8f9fa !important;
    padding: 10px 0 !important;
}

/* 일요일 색상 */
.fc-day-sun .fc-col-header-cell-cushion {
    color: #FF8F8F !important;
}

/* 토요일 색상 */
.fc-day-sat .fc-col-header-cell-cushion {
    color: #8AAAE5 !important;
}

/* 날짜 셀 스타일링 */
.fc-daygrid-day {
    transition: background-color 0.2s;
}

.fc-daygrid-day:hover {
    background-color: #f8f9fa !important;
}

/* 오늘 날짜 스타일링 */
.fc-day-today {
    background-color: rgba(144, 166, 132, 0.1) !important;
}

/* 이벤트 스타일링 */
.fc-event {
    border-radius: 4px !important;
    padding: 2px 4px !important;
    margin: 1px 0 !important;
    border: none !important;
}

/* 더보기 버튼 스타일링 */
.fc-more-link {
    color: #756AB6 !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# 캘린더 표시
calendar(events=events, options=calendar_options, key="calendar")

# 새 일정 추가 폼
st.divider()
st.subheader("새 일정 추가")

col1, col2 = st.columns(2)

with col1:
    event_title = st.text_input("일정 제목", placeholder="일정 제목을 입력하세요")
    start_date = st.date_input("시작 날짜", datetime.date.today())
    end_date = st.date_input("종료 날짜", datetime.date.today())

with col2:
    event_description = st.text_area("설명", placeholder="일정 설명을 입력하세요")
        # color picker를 드롭다운으로 변경
    color_name = st.selectbox(
        "색상 선택",
        options=list(COLOR_MAPPING.keys()),
        format_func=lambda x: x
    )
    event_color = COLOR_MAPPING[color_name]  # 선택된 색상명을 hex 코드로 변환

if st.button("일정 추가", use_container_width=True,type="primary"):
    if event_title:
        if start_date <= end_date:
            add_event(
                event_title,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                event_color,
                event_description
            )
            st.success("✅ 일정이 추가되었습니다!")
            st.balloons()
            st.experimental_rerun()
        else:
            st.error("종료일이 시작일보다 빠를 수 없습니다!")
    else:
        st.error("일정 제목을 입력해주세요!")
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

# 공휴일 정보 (2024년 12월 ~ 2025년)
KOREAN_HOLIDAYS = [
    # 2024년 12월
    {"title": "성탄절", "date": "2024-12-25"},
    
    # 2025년
    {"title": "신정", "date": "2025-01-01"},
    {"title": "설날", "date": "2025-01-28"},
    {"title": "설날 연휴", "date": "2025-01-29"},
    {"title": "설날 연휴", "date": "2025-01-30"},
    {"title": "삼일절", "date": "2025-03-01"},
    {"title": "어린이날", "date": "2025-05-05"},
    {"title": "부처님오신날", "date": "2025-05-06"},
    {"title": "현충일", "date": "2025-06-06"},
    {"title": "광복절", "date": "2025-08-15"},
    {"title": "추석", "date": "2025-10-04"},
    {"title": "추석 연휴", "date": "2025-10-05"},
    {"title": "추석 연휴", "date": "2025-10-06"},
    {"title": "개천절", "date": "2025-10-03"},
    {"title": "한글날", "date": "2025-10-09"},
    {"title": "성탄절", "date": "2025-12-25"}
]

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

def main():
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
            'backgroundColor': row['color'],
            'borderColor': row['color'],
            'textColor': '#FFFFFF'
        })

    # 공휴일 이벤트 추가
    holiday_events = []
    for holiday in KOREAN_HOLIDAYS:
        holiday_events.append({
            'title': holiday['title'],
            'start': holiday['date'],
            'end': holiday['date'],
            'display': 'background',
            'backgroundColor': '#fff5f5',
            'classNames': ['holiday-event'],
            'textColor': '#FF0000'
        })

    # 모든 이벤트 합치기
    all_events = events + holiday_events

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
        "themeSystem": "standard",
        
        # 버튼 텍스트
        "buttonText": {
            "today": "오늘",
            "month": "월",
            "week": "주",
            "day": "일"
        },
        
        # 날짜/시간 포맷
        "titleFormat": {
            "year": "numeric",
            "month": "long"
        },
        "dayHeaderFormat": { "weekday": "short" },
        "slotLabelFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "hour12": False
        },
        
        # 이벤트 표시 설정
        "eventDisplay": "block",
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "meridiem": False
        },
        
        # 기타 설정
        "firstDay": 0,
        "dayMaxEvents": True,
        "nowIndicator": True,
        "now": datetime.datetime.now().strftime("%Y-%m-%d"),
        
        # 주말 처리
        "weekends": True,
        "businessHours": {
            "daysOfWeek": [1, 2, 3, 4, 5]
        }
    }

    # 캘린더 스타일
    st.markdown("""
    <style>
    /* 캘린더 헤더 */
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

    /* 오늘 버튼 */
    .fc-today-button {
        background-color: #94A684 !important;
    }

    /* 제목 */
    .fc-toolbar-title {
        color: #333333 !important;
        font-size: 1.5em !important;
        font-weight: 600 !important;
    }

    /* 요일 헤더 */
    .fc-col-header-cell {
        background-color: #f8f9fa !important;
        padding: 10px 0 !important;
    }

    /* 주말 스타일링 */
    .fc-day-sun .fc-daygrid-day-frame, 
    .fc-day-sat .fc-daygrid-day-frame {
        background-color: #fff5f5 !important;
    }

    .fc-day-sun .fc-daygrid-day-number,
    .fc-day-sat .fc-daygrid-day-number {
        color: #FF0000 !important;
        font-weight: 500 !important;
    }

    /* 공휴일 스타일링 */
    .holiday-event {
        background-color: #fff5f5 !important;
        border: none !important;
    }

    .holiday-event .fc-event-title {
        color: #FF0000 !important;
        font-size: 0.85em !important;
        font-weight: 500 !important;
    }

    /* 이벤트 스타일링 */
    .fc-event {
        border-radius: 4px !important;
        padding: 2px 4px !important;
        margin: 1px 0 !important;
    }

    /* 더보기 링크 */
    .fc-more-link {
        color: #756AB6 !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 캘린더 표시
    calendar(events=all_events, options=calendar_options, key="calendar")

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
        color_name = st.selectbox(
            "색상 선택",
            options=list(COLOR_MAPPING.keys()),
            format_func=lambda x: x
        )
        event_color = COLOR_MAPPING[color_name]

    if st.button("일정 추가", use_container_width=True, type="primary"):
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

if __name__ == "__main__":
    main()

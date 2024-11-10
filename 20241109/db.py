# db.py
import sqlite3
import os
import pandas as pd

def delete_all_events():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('DELETE FROM events')
    conn.commit()
    conn.close()

def create_database():
    # 데이터베이스 파일이 있는지 확인
    if not os.path.exists('calendar.db'):
        # 데이터베이스 연결
        conn = sqlite3.connect('calendar.db')
        c = conn.cursor()
        
        # events 테이블 생성
        c.execute('''
            CREATE TABLE IF NOT EXISTS events
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             start_date DATE NOT NULL,
             end_date DATE NOT NULL,
             color TEXT,
             description TEXT)
        ''')
        
        # 샘플 데이터 추가 (선택사항)
        c.execute('''
            INSERT INTO events (title, start_date, end_date, color, description)
            VALUES (?, ?, ?, ?, ?)
        ''', ('샘플 일정', '2024-11-10', '2024-11-15', '#FF6B6B', '샘플 일정입니다.'))
        
        conn.commit()
        conn.close()
        print("데이터베이스가 성공적으로 생성되었습니다.")

def init_db():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    
    # events 테이블이 없으면 생성
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
    df = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return df

def delete_event(event_id):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

def update_event(event_id, title, start_date, end_date, color, description):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('''
        UPDATE events 
        SET title = ?, start_date = ?, end_date = ?, color = ?, description = ?
        WHERE id = ?
    ''', (title, start_date, end_date, color, description, event_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
import sqlite3

DB_NAME = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_requests (
            user_id INTEGER PRIMARY KEY,
            admin_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_promotion(text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO promotions (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def remove_promotion(promo_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM promotions WHERE text = ?", (promo_text,))
    conn.commit()
    conn.close()

def get_promotions(with_ids=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if with_ids:
        cursor.execute("SELECT id, text FROM promotions")
        promotions = cursor.fetchall()  # Вернет [(id, "текст акции"), ...]
    else:
        cursor.execute("SELECT text FROM promotions")
        promotions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return promotions

def add_subscriber(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def remove_subscriber(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_subscribers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM subscribers")
    subscribers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return subscribers

def add_chat_request(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO chat_requests (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def assign_admin_to_chat(user_id, admin_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE chat_requests SET admin_id = ? WHERE user_id = ?", (admin_id, user_id))
    conn.commit()
    conn.close()

def get_chat_request(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id FROM chat_requests WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_chat_request_for_admin(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM chat_requests WHERE admin_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def end_chat(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_requests WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# Инициализация базы данных при старте
init_db()
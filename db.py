import sqlite3
from pathlib import Path

DB_PATH = Path("chatbot.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        prompt_variant_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS prompt_variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        template TEXT,
        weight REAL DEFAULT 1.0
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS reward_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variant_id INTEGER,
        feedback_score REAL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def seed_variants():
    conn = get_conn()
    cur = conn.cursor()
    variants = [
        ("concise", "You are an expert in affiliate marketing. The user asked: '{user_question}'. Explain why creatives are crucial in affiliate marketing in concise bullet points with one real-world example and one actionable tip."),
        ("example-heavy", "You are a marketer. The user asked: '{user_question}'. Focus on real-world examples to explain why creatives matter in affiliate marketing. Include one actionable tip."),
        ("story-driven", "Tell a short story about an affiliate marketer. The user question: '{user_question}'. Through the story, surface why creatives are essential, ending with a practical suggestion.")
    ]
    for name, template in variants:
        cur.execute(
            "INSERT OR IGNORE INTO prompt_variants (name, template, weight) VALUES (?, ?, ?)",
            (name, template, 1.0)
        )
    conn.commit()
    conn.close()

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "papers.db"

FIELDS = ["purpose", "methods", "results", "limitations", "future_ideas"]


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            source_filename TEXT,
            uploaded_at TEXT NOT NULL,
            purpose TEXT,
            methods TEXT,
            results TEXT,
            limitations TEXT,
            future_ideas TEXT,
            keywords TEXT,
            raw_text TEXT
        )"""
    )
    existing_cols = [r["name"] for r in conn.execute("PRAGMA table_info(papers)").fetchall()]
    if "user_id" not in existing_cols:
        conn.execute("ALTER TABLE papers ADD COLUMN user_id INTEGER")
    conn.commit()
    conn.close()


def create_user(username: str, password_hash: str) -> int:
    conn = get_connection()
    is_first_user = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"] == 0
    conn.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, datetime.now().isoformat(timespec="seconds")),
    )
    user_id = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()["id"]
    if is_first_user:
        # Claim any papers created before multi-user accounts existed.
        conn.execute("UPDATE papers SET user_id = ? WHERE user_id IS NULL", (user_id,))
    conn.commit()
    conn.close()
    return user_id


def get_user_by_username(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row


def insert_paper(user_id, title, source_filename, summary, raw_text):
    conn = get_connection()
    conn.execute(
        """INSERT INTO papers
           (user_id, title, source_filename, uploaded_at, purpose, methods, results, limitations, future_ideas, keywords, raw_text)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            title,
            source_filename,
            datetime.now().isoformat(timespec="seconds"),
            summary.get("purpose", ""),
            summary.get("methods", ""),
            summary.get("results", ""),
            summary.get("limitations", ""),
            summary.get("future_ideas", ""),
            ", ".join(summary.get("keywords", [])),
            raw_text,
        ),
    )
    conn.commit()
    conn.close()


def list_papers(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM papers WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_paper(user_id, paper_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM papers WHERE id = ? AND user_id = ?", (paper_id, user_id)
    ).fetchone()
    conn.close()
    return row


def search_papers(user_id, query):
    conn = get_connection()
    like = f"%{query}%"
    rows = conn.execute(
        """SELECT * FROM papers WHERE user_id = ? AND (
           title LIKE ? OR purpose LIKE ? OR methods LIKE ? OR results LIKE ?
           OR limitations LIKE ? OR future_ideas LIKE ? OR keywords LIKE ?)
           ORDER BY uploaded_at DESC""",
        (user_id, like, like, like, like, like, like, like),
    ).fetchall()
    conn.close()
    return rows


def delete_paper(user_id, paper_id):
    conn = get_connection()
    conn.execute("DELETE FROM papers WHERE id = ? AND user_id = ?", (paper_id, user_id))
    conn.commit()
    conn.close()

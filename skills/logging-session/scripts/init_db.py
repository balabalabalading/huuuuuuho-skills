"""Initialize the session-log SQLite database."""
import sqlite3
import sys
import os

from config_loader import load_config


def init_db(db_path):
    if os.path.exists(db_path):
        print(f"Database already exists: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dev_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at DATETIME DEFAULT (datetime('now')),
        project_name TEXT NOT NULL,
        session_id TEXT NOT NULL,
        parent_id INTEGER DEFAULT NULL,
        task_category TEXT,
        user_query TEXT NOT NULL,
        thought_process TEXT,
        final_result TEXT,
        file_paths TEXT,
        git_hash TEXT,
        extra_metadata TEXT,
        FOREIGN KEY (parent_id) REFERENCES dev_logs (id)
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_project_name ON dev_logs(project_name)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_session_id ON dev_logs(session_id)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_created_at ON dev_logs(created_at)
    """)

    conn.commit()
    conn.close()
    print(f"Database created: {db_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        config = load_config()
        db_path = config["db_path"]
    init_db(db_path)

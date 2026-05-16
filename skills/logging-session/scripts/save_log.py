"""Save a session log entry to the SQLite database."""
import sqlite3
import json
import sys
import os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))


def save_log(db_path, project, session, query, thought, result,
             parent=None, category=None, files=None, git=None, meta=None):
    now_cst = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """
    INSERT INTO dev_logs (
        created_at, project_name, session_id, parent_id, task_category,
        user_query, thought_process, final_result,
        file_paths, git_hash, extra_metadata
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = (
        now_cst,
        project,
        session,
        parent,
        category,
        query,
        thought,
        result,
        ",".join(files) if files else None,
        git,
        json.dumps(meta, ensure_ascii=False) if meta else None
    )

    cursor.execute(sql, data)
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Save a session log entry")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--query", required=True, help="User query / task description")
    parser.add_argument("--thought", default="", help="Thought process / analysis")
    parser.add_argument("--result", default="", help="Final result / outcome")
    parser.add_argument("--parent", type=int, default=None, help="Parent log entry ID")
    parser.add_argument("--category", default=None, help="Task category")
    parser.add_argument("--files", nargs="*", default=None, help="Related file paths")
    parser.add_argument("--git", default=None, help="Git commit hash")
    parser.add_argument("--meta", default=None, help="Extra metadata as JSON string")

    args = parser.parse_args()

    meta = json.loads(args.meta) if args.meta else None

    log_id = save_log(
        args.db, args.project, args.session, args.query,
        args.thought, args.result, args.parent, args.category,
        args.files, args.git, meta
    )
    print(f"Log entry saved with ID: {log_id}")

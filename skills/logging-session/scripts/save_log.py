"""Save a session log entry to the SQLite database."""
import sqlite3
import json
import sys
import os
from config_loader import load_config
from time_utils import local_now_str


def save_log(db_path, project, session, query, thought, result,
             parent=None, category=None, files=None, git=None, meta=None):
    now_local = local_now_str()

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
        now_local,
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
    parser.add_argument("--db", default=None, help="Path to SQLite database (defaults to config.json)")
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

    db_path = args.db
    if not db_path:
        config = load_config()
        db_path = config["db_path"]

    if not db_path:
        print("错误：未指定数据库路径。请通过 --db 指定，或在 config.json 中配置 db_path。", file=sys.stderr)
        sys.exit(1)

    meta = None
    if args.meta:
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError as e:
            print(f"警告：--meta 参数不是有效的 JSON，已忽略: {e}", file=sys.stderr)

    log_id = save_log(
        db_path, args.project, args.session, args.query,
        args.thought, args.result, args.parent, args.category,
        args.files, args.git, meta
    )
    print(f"Log entry saved with ID: {log_id}")

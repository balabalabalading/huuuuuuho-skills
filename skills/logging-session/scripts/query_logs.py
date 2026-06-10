"""Query and format session logs from the SQLite database."""
import sqlite3
import json
import sys
import os

from config_loader import load_config
from time_utils import local_day_start_str


def _normalize_date(d):
    """Convert YYYYMMDD to YYYY-MM-DD. Pass through if already formatted."""
    if d and len(d) == 8 and d.isdigit():
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return d


def query_logs(db_path, project=None, days=7, session_id=None, limit=100,
              start_date=None, end_date=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM dev_logs WHERE 1=1"
    params = []

    if start_date and end_date:
        start_date = _normalize_date(start_date)
        end_date = _normalize_date(end_date)
        query += " AND created_at >= ? AND created_at < datetime(?, '+1 day')"
        params.append(start_date)
        params.append(end_date)
    elif start_date:
        start_date = _normalize_date(start_date)
        query += " AND created_at >= ?"
        params.append(start_date)
    elif end_date:
        end_date = _normalize_date(end_date)
        query += " AND created_at < datetime(?, '+1 day')"
        params.append(end_date)
    elif days:
        query += " AND created_at >= ?"
        params.append(local_day_start_str(days))

    if project:
        query += " AND project_name = ?"
        params.append(project)

    if session_id:
        query += " AND session_id = ?"
        params.append(session_id)

    query += " ORDER BY created_at ASC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = [dict(row) for row in rows]
    conn.close()
    return results


def format_markdown(logs, title="Session Log"):
    output = f"# {title}\n\n"
    if not logs:
        output += "*No records found for the specified period.*\n"
        return output
    current_date = None

    for log in logs:
        created = log["created_at"]
        date_part = created[:10] if created else "unknown"

        if date_part != current_date:
            current_date = date_part
            output += f"## {current_date}\n\n"

        output += f"### {log['user_query']}\n"
        output += f"- **项目**: {log['project_name']}\n"
        output += f"- **分类**: {log.get('task_category', '-') or '-'}\n"
        output += f"- **会话**: {log['session_id']}\n"
        if log.get('parent_id'):
            output += f"- **父记录**: #{log['parent_id']}\n"
        output += f"\n**思考过程**:\n{log.get('thought_process', '-') or '-'}\n\n"
        output += f"**最终结果**:\n{log.get('final_result', '-') or '-'}\n\n"
        if log.get('file_paths'):
            output += f"**相关文件**: {log['file_paths']}\n\n"
        if log.get('git_hash'):
            output += f"**Git**: `{log['git_hash']}`\n\n"
        output += "---\n\n"

    return output


def format_for_ai(logs):
    output = ""
    for log in logs:
        output += f"时间: {log['created_at']}\n"
        output += f"项目: {log['project_name']}\n"
        output += f"问题: {log['user_query']}\n"
        output += f"思考过程: {log.get('thought_process', '-') or '-'}\n"
        output += f"最终结果: {log.get('final_result', '-') or '-'}\n"
        output += "------------------\n"
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query session logs")
    parser.add_argument("--db", default=None, help="Path to SQLite database (defaults to config.json)")
    parser.add_argument("--project", default=None, help="Filter by project name")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (0 = all records)")
    parser.add_argument("--start-date", default=None, help="Start date YYYYMMDD (inclusive)")
    parser.add_argument("--end-date", default=None, help="End date YYYYMMDD (inclusive)")
    parser.add_argument("--session", default=None, help="Filter by session ID")
    parser.add_argument("--limit", type=int, default=100, help="Max results")
    parser.add_argument("--format", choices=["markdown", "ai", "json"], default="markdown",
                        help="Output format")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    db_path = args.db
    if not db_path:
        config = load_config()
        db_path = config["db_path"]

    if not db_path:
        print("错误：未指定数据库路径。请通过 --db 指定，或在 config.json 中配置 db_path。", file=sys.stderr)
        sys.exit(1)

    logs = query_logs(db_path, args.project, args.days, args.session, args.limit,
                      args.start_date, args.end_date)

    if args.format == "markdown":
        content = format_markdown(logs)
    elif args.format == "ai":
        content = format_for_ai(logs)
    else:
        content = json.dumps(logs, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Output saved to: {args.output}")
    else:
        print(content)

"""Generate weekly project summary from session logs."""
import sqlite3
import json
import sys
from collections import Counter

from config_loader import load_config
from time_utils import local_day_start_str, local_date_str


def _normalize_date(d):
    """Convert YYYYMMDD to YYYY-MM-DD. Pass through if already formatted."""
    if d and len(d) == 8 and d.isdigit():
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return d


def query_logs(db_path, project=None, days=7, limit=200,
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
        query += " AND created_at >= ? AND created_at < ?"
        params.append(local_day_start_str(days))
        params.append(local_day_start_str(0))

    if project:
        query += " AND project_name = ?"
        params.append(project)

    query += " ORDER BY project_name, created_at DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results


def build_summary(logs, days=7, start_date=None, end_date=None):
    if start_date and end_date:
        end_str = _normalize_date(end_date)
        start_str = _normalize_date(start_date)
    else:
        end_str = local_date_str(1)
        start_str = local_date_str(days)

    if not logs:
        return {
            "period": {"start_date": start_str, "end_date": end_str, "days": days},
            "total_entries": 0,
            "total_projects": 0,
            "projects": [],
        }

    projects = {}
    for log in logs:
        pname = log["project_name"]
        if pname not in projects:
            projects[pname] = {"entries": [], "category_counter": Counter()}
        projects[pname]["entries"].append(log)
        cat = log.get("task_category") or "未分类"
        projects[pname]["category_counter"][cat] += 1

    project_list = []
    for name, data in projects.items():
        sessions = []
        for entry in data["entries"]:
            created = entry["created_at"] or ""
            sessions.append({
                "date": created[:10] if created else "unknown",
                "session_id": entry["session_id"],
                "category": entry.get("task_category") or "未分类",
                "user_query": entry["user_query"],
                "final_result": entry.get("final_result") or "",
            })
        project_list.append({
            "name": name,
            "total_entries": len(data["entries"]),
            "categories": dict(data["category_counter"]),
            "sessions": sessions,
        })

    project_list.sort(key=lambda p: p["total_entries"], reverse=True)

    return {
        "period": {"start_date": start_str, "end_date": end_str, "days": days},
        "total_entries": len(logs),
        "total_projects": len(project_list),
        "projects": project_list,
    }


def _truncate(text, max_len):
    if not text:
        return "-"
    text = text.replace("\n", " ").replace("|", "/")
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def format_markdown(summary):
    period = summary["period"]
    output = f"# 工作周报 ({period['start_date']} ~ {period['end_date']})\n\n"

    if summary["total_entries"] == 0:
        output += f"没有找到过去 {period['days']} 天的记录。\n"
        return output

    output += "## 概览\n\n"
    output += f"- **总记录数**: {summary['total_entries']} 条\n"
    output += f"- **涉及项目**: {summary['total_projects']} 个\n"
    output += f"- **统计周期**: 过去 {period['days']} 天\n\n"

    for proj in summary["projects"]:
        output += f"## {proj['name']} — {proj['total_entries']} 条记录\n\n"

        # Category breakdown table
        output += "### 任务分类\n\n"
        output += "| 分类 | 数量 |\n"
        output += "|------|------|\n"
        for cat, count in sorted(proj["categories"].items(), key=lambda x: x[1], reverse=True):
            output += f"| {cat} | {count} |\n"
        output += "\n"

        # Session details table
        output += "### 详细记录\n\n"
        output += "| 日期 | 分类 | 内容 | 结果 |\n"
        output += "|------|------|------|------|\n"
        for s in proj["sessions"]:
            date_short = s["date"][5:] if len(s["date"]) >= 10 else s["date"]
            query = _truncate(s["user_query"], 50)
            result = _truncate(s["final_result"], 60)
            output += f"| {date_short} | {s['category']} | {query} | {result} |\n"
        output += "\n"

    return output


def format_json(summary):
    return json.dumps(summary, ensure_ascii=False, indent=2)


def format_ai(summary):
    period = summary["period"]
    if summary["total_entries"] == 0:
        return f"过去 {period['days']} 天没有找到任何工作记录。"

    lines = [
        f"工作周报 ({period['start_date']} ~ {period['end_date']})",
        f"总记录: {summary['total_entries']} 条, 涉及 {summary['total_projects']} 个项目",
        "",
    ]
    for proj in summary["projects"]:
        lines.append(f"项目: {proj['name']} ({proj['total_entries']} 条)")
        cats = ", ".join(
            f"{k}({v})" for k, v in sorted(
                proj["categories"].items(), key=lambda x: x[1], reverse=True
            )
        )
        lines.append(f"  分类: {cats}")
        for s in proj["sessions"]:
            query = _truncate(s["user_query"], 80)
            result = _truncate(s["final_result"], 80)
            lines.append(f"  [{s['date']}] [{s['category']}] {query}")
            if result != "-":
                lines.append(f"    结果: {result}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate weekly project summary from session logs")
    parser.add_argument("--db", default=None, help="Path to SQLite database (defaults to config.json)")
    parser.add_argument("--project", default=None, help="Filter by project name")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (0 = all records, default: 7)")
    parser.add_argument("--start-date", default=None, help="Start date YYYYMMDD (inclusive)")
    parser.add_argument("--end-date", default=None, help="End date YYYYMMDD (inclusive)")
    parser.add_argument("--limit", type=int, default=200, help="Max rows to fetch (default: 200)")
    parser.add_argument("--format", choices=["markdown", "ai", "json"], default="markdown",
                        help="Output format (default: markdown)")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    db_path = args.db
    if not db_path:
        config = load_config()
        db_path = config["db_path"]

    if not db_path:
        print("错误：未指定数据库路径。请通过 --db 指定，或在 config.json 中配置 db_path。", file=sys.stderr)
        sys.exit(1)

    logs = query_logs(db_path, args.project, args.days, args.limit,
                      args.start_date, args.end_date)
    summary = build_summary(logs, args.days, args.start_date, args.end_date)

    if args.format == "json":
        content = format_json(summary)
    elif args.format == "ai":
        content = format_ai(summary)
    else:
        content = format_markdown(summary)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Output saved to: {args.output}")
    else:
        print(content)
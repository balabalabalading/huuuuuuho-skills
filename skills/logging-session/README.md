# logging-session

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

Record and query AI coding session logs — what you asked, how it was solved, and the result. Stores entries to a local SQLite database in your Obsidian vault for later summarization and review.

## Features

- **Automatic logging via Stop hook**: When a Claude Code session ends, the Stop hook triggers automatic session summarization — no manual action needed
- **Structured records**: Captures project name, user query, thought process, final result, file paths, git hash, and more
- **Flexible querying**: Query by project, date range, or session ID; output as markdown, AI-readable text, or JSON
- **Obsidian integration**: Export summaries as Obsidian notes directly into your vault
- **Thread support**: Link related sessions via `parent_id` to build conversation threads

## Installation

### Via Claude Code Marketplace

```bash
git clone https://github.com/balabalabalading/huuuuuuho-skills.git ~/.claude/skills/huuuuuuho-skills
```

Then in Claude Code:
```
/plugin marketplace add ~/.claude/skills/huuuuuuho-skills
/plugin install huuuuuuho-skills@logging-session
```

### Configuration

The database path and Obsidian vault path are defined in `config.json` with these defaults:

```json
{
  "db_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life/dev_knowledge.db",
  "obsidian_vault_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life"
}
```

To customize, edit `config.json`. Scripts will read from it automatically — no need to pass `--db` manually.

### Initialize the database

```bash
python3 ~/.claude/skills/huuuuuuho-skills/skills/logging-session/scripts/init_db.py
```

The script reads the database path from `config.json` automatically.

### Set up the Stop hook

Add the following to `~/.claude/settings.json` to enable automatic session logging:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "你是一个负责检查会话是否真正可以结束的守卫。下面是本次 Stop hook 的输入 JSON：\n\n$ARGUMENTS\n\n规则：\n1. 如果这是第一次触发 Stop hook（stop_hook_active 字段为 false 或不存在），你必须返回 {\"ok\": false, \"reason\": \"现在请运行 /logging-session，总结整个当前会话，并把总结结果发给用户。完成后你可以再次尝试结束会话。\"}。\n2. 如果 stop_hook_active 为 true，说明上一次 Stop hook 已经要求你执行 /logging-session，这一轮就允许结束：返回 {\"ok\": true}。\n仅返回一个 JSON 对象，不要说其它话。"
          }
        ]
      }
    ]
  }
}
```

## Usage

### Recording a session

Just finish your work — the Stop hook captures it automatically. You can also trigger manually:

- "Record this session"
- "Log this conversation"
- "/logging-session"

### Querying sessions

```bash
SCRIPTS=~/.claude/skills/huuuuuuho-skills/skills/logging-session/scripts

# Last 7 days for a specific project (markdown)
python3 $SCRIPTS/query_logs.py \
  --project "my-app" --days 7 --format markdown

# Today's logs across all projects
python3 $SCRIPTS/query_logs.py \
  --days 1 --format markdown

# Export to Obsidian note
python3 $SCRIPTS/query_logs.py \
  --days 7 --format markdown \
  --output ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/vault4life/Weekly-$(date +%Y-W%V).md
```

## Database Schema

```sql
CREATE TABLE dev_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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
);
```

## Task Categories

| Category | Description |
|----------|-------------|
| `bugfix` | Fixed a bug or error |
| `feature` | Added new functionality |
| `refactor` | Restructured code without changing behavior |
| `debug` | Investigated an issue |
| `setup` | Project setup, configuration |
| `docs` | Documentation work |
| `test` | Writing or fixing tests |
| `other` | Anything else |

## Related Article

[写个 Hook 截胡大模型：将零散的 AI 对话重塑为本地知识资产](https://mp.weixin.qq.com/s/jGSc1NjR_DPMWhZEYi8OJQ)

## License

[MIT](../LICENSE)

---

<a id="chinese"></a>

记录和查询 AI 编码会话日志 — 你问了什么、怎么解决的、结果如何。将会话摘要存储到本地 SQLite 数据库，方便后续查询和回顾。

## 功能特性

- **Stop hook 自动记录**：Claude Code 会话结束时自动触发总结，无需手动操作
- **结构化记录**：记录项目名称、用户问题、思考过程、最终结果、文件路径、git hash 等
- **灵活查询**：按项目、日期范围、会话 ID 查询；支持 markdown、AI 可读文本、JSON 三种输出格式
- **Obsidian 集成**：直接导出为 Obsidian 笔记到 vault 中
- **会话线程**：通过 `parent_id` 关联相关会话

## 安装

### 通过 Claude Code Marketplace

```bash
git clone https://github.com/balabalabalading/huuuuuuho-skills.git ~/.claude/skills/huuuuuuho-skills
```

在 Claude Code 中运行：
```
/plugin marketplace add ~/.claude/skills/huuuuuuho-skills
/plugin install huuuuuuho-skills@logging-session
```

### 自定义配置

数据库路径和 Obsidian vault 路径由 `config.json` 定义。默认值如下：

```json
{
  "db_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life/dev_knowledge.db",
  "obsidian_vault_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life"
}
```

如需自定义，修改 `config.json` 中的路径即可。后续脚本会自动读取，无需手动传 `--db`。

### 初始化数据库

```bash
python3 ~/.claude/skills/huuuuuuho-skills/skills/logging-session/scripts/init_db.py
```

脚本会自动从 `config.json` 读取数据库路径。

### 配置 Stop hook

在 `~/.claude/settings.json` 中添加 hook 配置即可在会话结束时自动记录。

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "你是一个负责检查会话是否真正可以结束的守卫。下面是本次 Stop hook 的输入 JSON：\n\n$ARGUMENTS\n\n规则：\n1. 如果这是第一次触发 Stop hook（stop_hook_active 字段为 false 或不存在），你必须返回 {\"ok\": false, \"reason\": \"现在请运行 /logging-session，总结整个当前会话，并把总结结果发给用户。完成后你可以再次尝试结束会话。\"}。\n2. 如果 stop_hook_active 为 true，说明上一次 Stop hook 已经要求你执行 /logging-session，这一轮就允许结束：返回 {\"ok\": true}。\n仅返回一个 JSON 对象，不要说其它话。"
          }
        ]
      }
    ]
  }
}
```


## 使用

### 记录会话

正常完成工作即可 — Stop hook 会自动捕获。也可以手动触发：
- "记录本次会话"
- "Log this conversation"
- /logging session

### 查询会话

```bash
SCRIPTS=~/.claude/skills/huuuuuuho-skills/skills/logging-session/scripts

# 最近 7 天指定项目的记录
python3 $SCRIPTS/query_logs.py \
  --project "my-app" --days 7 --format markdown

# 导出为 Obsidian 笔记
python3 $SCRIPTS/query_logs.py \
  --days 7 --format markdown \
  --output ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/vault4life/Weekly-$(date +%Y-W%V).md
```

## 任务分类

| 分类 | 说明 |
|------|------|
| `bugfix` | 修复 bug |
| `feature` | 新增功能 |
| `refactor` | 重构代码 |
| `debug` | 问题排查 |
| `setup` | 项目配置 |
| `docs` | 文档工作 |
| `test` | 测试 |
| `other` | 其他 |

## 相关文章

[写个 Hook 截胡大模型：将零散的 AI 对话重塑为本地知识资产](https://mp.weixin.qq.com/s/jGSc1NjR_DPMWhZEYi8OJQ)

## 许可证

[MIT](../LICENSE)

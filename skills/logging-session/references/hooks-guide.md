# Hooks Setup Guide

This guide explains how to set up automatic session logging via Claude Code hooks.

## How it works

The Stop hook uses a two-phase mechanism:

1. **First Stop**: When Claude tries to end the session, the prompt hook intercepts and returns `{"ok": false}`, instructing Claude to run `/logging-session` first.
2. **Second Stop**: After logging the session, Claude tries to end again. This time `stop_hook_active` is true, so the hook returns `{"ok": true}` and the session ends.

From the user's perspective: you finish a conversation, and Claude automatically logs it before closing — no manual action needed.

## Prompt hook configuration

Add this to `~/.claude/settings.json`:

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

The `$ARGUMENTS` variable is automatically filled by Claude Code with the hook's input JSON, which includes the `stop_hook_active` field.

## Verifying hooks are working

After ending a session, check the database:

```bash
python3 /path/to/logging-session/scripts/query_logs.py \
  --db ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/vault4life/dev_knowledge.db \
  --days 1 --format ai
```

You should see the auto-logged entry.

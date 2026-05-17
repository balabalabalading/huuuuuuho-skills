# huuuuuho-skills

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

My personal collection of Skills — open-source tools that extend Agent's capabilities for content creation, development logging, and productivity workflows.

## Skills Overview

| Skill                 | Description                                                                        | README                                       | Article                                                   |
| --------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------- |
| **mp-article-writor** | Generate long-form WeChat Official Account articles with a 9-step writing workflow | [README](skills/mp-article-writor/README.md) | [Link](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ) |
| **logging-session**   | Record and query AI coding session logs to your Obsidian vault                     | [README](skills/logging-session/README.md)   | [Link](https://mp.weixin.qq.com/s/jGSc1NjR_DPMWhZEYi8OJQ) |
| **article2ticktick**  | Convert tech newsletter articles to TickTick todos with auto-categorization        | [README](skills/article2ticktick/README.md)  | [Link](https://mp.weixin.qq.com/s/xbvFmOwk0SwdWMw4BUczSg) |

## Quick Start

### Install all skills at once

In Claude Code:
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
/plugin install logging-session@huuuuuuho
/plugin install article2ticktick@huuuuuuho
```

### Install a single skill

```
/plugin install <skill-name>@huuuuuuho
```

Replace `<skill-name>` with `mp-article-writor`, `logging-session`, or `article2ticktick`.

## Repository Structure

```
huuuuuuho-skills/
├── README.md
├── LICENSE
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    ├── mp-article-writor/
    │   ├── README.md
    │   ├── SKILL.md
    │   └── references/
    ├── logging-session/
    │   ├── README.md
    │   ├── SKILL.md
    │   ├── scripts/
    │   ├── references/
    │   └── evals/
    └── article2ticktick/
        ├── README.md
        ├── SKILL.md
        └── scripts/
```

## License

[MIT](LICENSE)

---

<a id="chinese"></a>

我的 Skills 个人合集 — 扩展 Agent 在内容创作、开发日志记录、效率工作流方面的能力。

## Skills 一览

| Skill | 简介 | README | 公众号文章 |
|---|---|---|---|
| **mp-article-writor** | 公众号长文生成：9 步写作工作流，从素材到终稿 | [README](skills/mp-article-writor/README.md) | [链接](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ) |
| **logging-session** | AI 编码会话记录与查询，支持 Obsidian 集成 | [README](skills/logging-session/README.md) | _待补充_ |
| **article2ticktick** | 技术周报文章批量/单篇转滴答清单待办 | [README](skills/article2ticktick/README.md) | [链接](https://mp.weixin.qq.com/s/xbvFmOwk0SwdWMw4BUczSg) |

## 快速开始

### 一次性安装所有 Skills

在 Claude Code 中运行：
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
/plugin install logging-session@huuuuuuho
/plugin install article2ticktick@huuuuuuho
```

### 单独安装某个 Skill

```
/plugin install <skill-name>@huuuuuuho
```

将 `<skill-name>` 替换为 `mp-article-writor`、`logging-session` 或 `article2ticktick`。

## 仓库结构

```
huuuuuuho-skills/
├── README.md
├── LICENSE
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    ├── mp-article-writor/
    │   ├── README.md
    │   ├── SKILL.md
    │   └── references/
    ├── logging-session/
    │   ├── README.md
    │   ├── SKILL.md
    │   ├── scripts/
    │   ├── references/
    │   └── evals/
    └── article2ticktick/
        ├── README.md
        ├── SKILL.md
        └── scripts/
```

## 许可证

[MIT](LICENSE)

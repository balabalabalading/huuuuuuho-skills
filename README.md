# huuuuuho-skills

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

My personal collection of Skills — open-source tools that extend Agent's capabilities for content creation, development logging, and productivity workflows.

## Skills Overview

| Skill                 | Description                                                                        | README                                       | Article                                                   |
| --------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------- |
| **mp-article-writor** | Generate static WeChat articles with an 11-step writing and visual-production workflow | [README](skills/mp-article-writor/README.md) | [Link](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ) |
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

`mp-article-writor` 2.0 recommends two optional Guizang skills for complete static covers and body illustrations. See its [README](skills/mp-article-writor/README.md) for installation commands. Missing Guizang skills do not block article writing, but their visual outputs remain pending.

### Branch migration

The default branch is now `main`. The remote `master` branch remains available during the migration window. If an existing clone still tracks `master`, run:

```bash
git fetch origin
git switch main
git branch --set-upstream-to=origin/main main
```

The `master` branch will be removed after the migration window. New clones use `main` automatically.

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
| **mp-article-writor** | 微信公众号静态图文生成：11 步写作、视觉生产和交付工作流 | [README](skills/mp-article-writor/README.md) | [链接](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ) |
| **logging-session** | AI 编码会话记录与查询，支持 Obsidian 集成 | [README](skills/logging-session/README.md) | [链接](https://mp.weixin.qq.com/s/jGSc1NjR_DPMWhZEYi8OJQ) |
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

`mp-article-writor` 2.0 推荐安装两个归藏 Skill，以完成静态双封面和正文插图生产。安装命令见其 [README](skills/mp-article-writor/README.md)。缺少归藏 Skill 不影响文章写作，对应视觉素材会保留为待完成项目。

### 分支迁移

仓库默认分支已经切换为 `main`。迁移期间会暂时保留远程 `master` 分支。已有本地副本如果仍跟踪 `master`，请执行：

```bash
git fetch origin
git switch main
git branch --set-upstream-to=origin/main main
```

迁移窗口结束后会删除 `master` 分支，新克隆的仓库会自动使用 `main`。

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

# article2ticktick

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

A Skill that converts technical newsletter articles (batch or single) into [TickTick](https://ticktick.com/) todos with automatic categorization and tagging.

<p align="center">
  <img width="800" alt="Screenshot" src="https://github.com/user-attachments/assets/9dbcd7e9-b3e5-443c-a86f-efa386143390">
  <br>
  <em>Effect after adding to TickTick</em>
</p>

## Features

- **Branch A: Batch Newsletter** — Paste an entire newsletter issue, AI auto-categorizes and batch-adds to TickTick
- **Branch B: Single Article** — Share any article URL, AI infers category, generates a recommendation, and adds to TickTick

## Installation

### Via Claude Code Marketplace

```bash
git clone https://github.com/balabalabalading/huuuuuuho-skills.git ~/.claude/skills/huuuuuuho-skills
```

Then in Claude Code:
```
/plugin marketplace add ~/.claude/skills/huuuuuuho-skills
/plugin install huuuuuuho-skills@article2ticktick
```

### Local testing

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install huuuuuuho-skills@article2ticktick
```

## Usage

### Create lists in TickTick first

TickTick does not support creating lists via URL scheme — manually create the required lists first, or all todos fall into Inbox.

### Trigger the Skill

- `Help me add this newsletter to TickTick` → triggers Branch A (batch)
- `Add this article to TickTick: [URL]` → triggers Branch B (single)

## Classification System

Level-2 categories map to TickTick list names; Level-3 categories map to tags.

| Level-2 (TickTick list) | Common Level-3 (tags) |
|---|---|
| SwiftUI | Basic components & API, Layout & animation, State management, Navigation, System integration, Performance, App architecture |
| Swift Language | Concurrency & async, Language features, Cross-platform & embedded |
| Data & Persistence | SwiftData, CloudKit, Database |
| iOS & macOS Engineering | System capabilities, App Store & publishing, Resource management |
| Dev Tools & Workflow | Package managers, Xcode & project setup, Testing & debugging, CLI & server-side |
| AI-Assisted Development | Agent coding practices, Tools & configuration, On-device AI |
| Industry Insights | Hardware products |

## Standalone Script Usage

```bash
SCRIPTS=~/.claude/skills/huuuuuuho-skills/skills/article2ticktick/scripts

# Batch mode (dry-run preview)
echo "[markdown content]" | python3 $SCRIPTS/add_articles.py --dry-run

# Single article mode
python3 $SCRIPTS/add_articles.py \
  --task \
  --title "[Article Title](https://example.com)" \
  --list "SwiftUI" \
  --tags "State management" \
  --desc "A brief intro of the article..."
```

## Related Article

[利用 Skill 向滴答清单批量创建稍后读待办](https://mp.weixin.qq.com/s/xbvFmOwk0SwdWMw4BUczSg)

## License

[MIT](../LICENSE)

---

<a id="chinese"></a>

将技术周报文章（批量或单篇）转换为[滴答清单](https://dida365.com/)待办事项的 Skill，支持自动分类和标签。

<p align="center">
  <img width="800" alt="效果截图" src="https://github.com/user-attachments/assets/9dbcd7e9-b3e5-443c-a86f-efa386143390">
  <br>
  <em>添加到滴答清单后的效果</em>
</p>

## 功能

- **分支 A：批量周报** — 粘贴一整期周报，AI 自动整理分类，批量添加到滴答清单
- **分支 B：单篇文章** — 分享任意文章 URL，AI 推断分类、生成推荐语，一键添加

## 安装

### 通过 Claude Code Marketplace

```bash
git clone https://github.com/balabalabalading/huuuuuuho-skills.git ~/.claude/skills/huuuuuuho-skills
```

在 Claude Code 中运行：
```
/plugin marketplace add ~/.claude/skills/huuuuuuho-skills
/plugin install huuuuuuho-skills@article2ticktick
```

### 本地测试

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install huuuuuuho-skills@article2ticktick
```

## 使用

### 先在滴答清单创建列表

滴答清单不支持通过 Scheme URL 创建列表，请先手动创建好列表。

### 触发 Skill

- `帮我把这期周报添加到滴答清单` → 分支 A（批量）
- `把这篇文章添加到滴答清单：[URL]` → 分支 B（单篇）

## 分类体系

| 二级分类（列表名） | 常见三级分类（标签） |
|---|---|
| SwiftUI | 基础组件与 API、布局视觉与动画、状态管理与观察、导航与交互、系统集成与实战、性能与调试、应用架构 |
| Swift 语言 | 并发与异步、语言特性与底层原理、跨平台与嵌入式 |
| 数据与持久化 | SwiftData、CloudKit 与数据同步、数据库 |
| iOS 与 macOS 工程实践 | 系统能力与平台集成、App Store 与发布、资源管理、应用架构 |
| 开发工具与工作流 | 包管理器与依赖、Xcode 与项目工程、测试与调试、命令行与服务端 |
| AI 辅助开发 | Agent 编码实践、工具与配置、端侧 AI |
| 行业思考与视野 | 硬件产品 |

## 脚本直接使用

```bash
SCRIPTS=~/.claude/skills/huuuuuuho-skills/skills/article2ticktick/scripts

# 批量模式（预览）
echo "[markdown 内容]" | python3 $SCRIPTS/add_articles.py --dry-run

# 单篇模式
python3 $SCRIPTS/add_articles.py \
  --task \
  --title "[文章标题](https://example.com)" \
  --list "SwiftUI" \
  --tags "状态管理与观察" \
  --desc "文章简介..."
```

## 相关文章

[利用 Skill 向滴答清单批量创建稍后读待办](https://mp.weixin.qq.com/s/xbvFmOwk0SwdWMw4BUczSg)

## 许可证

[MIT](../LICENSE)

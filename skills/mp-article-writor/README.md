# mp-article-writor

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

A Claude Code Skill that helps content creators craft static long-form articles for WeChat Official Accounts (公众号). Covers an 11-step workflow from intent understanding to final article, static covers, explanatory illustrations, and delivery checks.

## Features

- **11-step article workflow**: Intent understanding → Style calibration → Outline and visual plan → Draft writing → Independent review → Fact-checking → Revision → Final self-check → Finished article → Static visual production → Delivery check
- **Independent review + fact-checking**: Subagent-powered reviews that detect AI-generated tone, logical gaps, structural symmetry, and factual accuracy
- **"Human voice" final check**: Evaluates whether the article reads like "a knowledgeable friend chatting" or "AI outputting information"
- **Style calibration**: Dual reference system (essay style analysis + writing style guide) to match your voice
- **Two illustration styles**: Choose Guizang social-card layouts or Guizang material illustrations during intake; WeChat cover pairs always use the social-card skill
- **Static-only delivery**: Produces a 21:9 main cover, a separately composed 1:1 share cover, body illustrations, editable files, prompts, and source records; no Live Photo or video output
- **Self-check checklist**: Four-layer quality gate — hard rules, style consistency, HKR scoring, human voice check

## Installation

### Via Claude Code Marketplace

In Claude Code:
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

For the complete static visual workflow, install both optional Guizang skills. They are recommended prerequisites and are not installed automatically:

```bash
npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill
npx skills add https://github.com/op7418/guizang-material-illustration --skill guizang-material-illustration
```

The writing workflow still runs when either skill is missing. Visual outputs covered by the missing skill are listed as pending; the workflow does not fall back to the previous prompt-only delivery.

Version 2.0 replaces the previous prompt-only illustration workflow with actual static visual production. The previous stable source remains available at the `mp-article-writor--v1.0.0` tag.

### Local testing

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

## Usage

Describe your writing needs in Claude Code and the Skill triggers automatically:

- "Help me write a WeChat article about XX"
- "Turn these materials into a blog post"
- "Write a draft for my newsletter"

The Skill follows a strict 11-step workflow, completing each step before moving to the next.

## Workflow

```
Step 1  Understand intent     → Confirm angle, depth, theme, materials, illustration style, and output folder
Step 2  Read references        → Calibrate voice (essay analysis + style guide)
Step 3  Design outline & style → Present outline and visual script, await confirmation
Step 4  Write first draft      → Follow all writing rules
Step 5  Independent review     → AI-tone detection, logic, structure, information density
Step 6  Fact-checking          → Article facts, visual evidence, sources, and permissions
Step 7  Revise draft           → Address feedback item by item
Step 8  Final self-check       → Article and visual-plan quality checklist
Step 9  Finalize               → Update file + self-check report + title suggestions
Step 10 Produce visuals        → Static WeChat cover pair + selected body-illustration style
Step 11 Delivery check         → Dimensions, paths, labels, data, permissions, and static-only outputs
```

## Customization

After installation, customize `SKILL.md` for your own writing:
- **Account name**: Search and replace with your own WeChat account name
- **Fixed footer**: Replace the promo section with your own content
- **Author voice**: Modify the "Author Voice" section
- **Reader profile**: Update the "Reader Profile" section
- **File paths**: Update save paths and front matter tags
- **Style analysis**: Replace `references/范文风格分析.md` with analysis of your own writing

## Related Article

[AI + Skill，能够让生成的文章去除 AI 味吗？](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ)

## License

[MIT](../LICENSE)

---

<a id="chinese"></a>

一个 Claude Code Skill，帮助自媒体创作者将素材整理为微信公众号静态图文长文。覆盖从意图理解、大纲和视觉脚本、初稿撰写到静态配图生产与交付检查的完整工作流。

## 功能特性

- **11 步文章工作流**：意图理解 → 风格校准 → 大纲和视觉脚本 → 初稿撰写 → 独立审读 → 事实核查 → 修改 → 终审自检 → 完成终稿 → 静态视觉生产 → 交付检查
- **独立审读 + 事实核查**：通过 subagent 对初稿进行 AI 味检测、逻辑连贯性检查、事实性核查
- **「活人感」终审**：判断文章读起来是「朋友在聊天」还是「AI 在输出」
- **风格校准**：范文分析 + 行文风格指南双重校准
- **两种正文插图风格**：在询问环节选择归藏 social-card 排版卡片或归藏 material 材质插图，公众号封面固定使用 social-card
- **全静态交付**：生成 21:9 主封面、单独构图的 1:1 分享封面、正文插图、可编辑文件、提示词和来源记录，不生成 Live Photo 或视频
- **自检清单**：硬性规则、风格一致性、HKR 质检、活人感四层检查

## 安装

### 通过 Claude Code Marketplace

在 Claude Code 中运行：
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

完整静态视觉工作流推荐安装以下两个归藏 Skill。它们不会随 mp-article-writor 自动安装：

```bash
npx skills add https://github.com/op7418/guizang-social-card-skill --skill guizang-social-card-skill
npx skills add https://github.com/op7418/guizang-material-illustration --skill guizang-material-illustration
```

缺少任一 Skill 时仍可完成文章写作，对应的视觉素材会被列为待完成项目，不会退回旧版提示词交付方式。

2.0 版本使用实际静态视觉生产替代旧版提示词配图流程。旧版稳定源码保留在 `mp-article-writor--v1.0.0` 标签。

### 本地测试

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

## 使用

在 Claude Code 中直接描述写作需求即可触发：

- 「帮我写一篇关于 XX 的公众号文章」
- 「把这些素材整理成推文」
- 「发公众号」

Skill 会按 11 步工作流依次执行。

## 工作流

```
Step 1  理解作者意图    → 确认切入角度、深度、主旨、素材、正文插图风格和输出目录
Step 2  阅读参考资料    → 校准语感（范文分析 + 风格指南）
Step 3  设计大纲和风格  → 呈现大纲和视觉脚本，等待确认
Step 4  编写初稿        → 按规则写作
Step 5  独立审读        → AI 味检测、逻辑、结构、信息密度
Step 6  事实核查        → 正文事实、视觉证据、素材来源和授权状态
Step 7  修改初稿        → 逐条处理反馈
Step 8  终审自检        → 文章和视觉脚本自检
Step 9  完成终稿        → 更新文件 + 自检报告 + 标题推荐
Step 10 生产静态视觉    → 公众号封面组合 + 已选正文插图风格
Step 11 交付检查        → 尺寸、路径、标签、数据、授权和静态输出
```

## 自定义配置

安装后修改 `SKILL.md` 中的以下内容：
- **公众号名称**、**固定结尾**、**作者声音**、**读者画像**、**文件保存路径**
- 将 `references/范文风格分析.md` 替换为你自己的风格分析

## 相关文章

[AI + Skill，能够让生成的文章去除 AI 味吗？](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ)

## 许可证

[MIT](../LICENSE)

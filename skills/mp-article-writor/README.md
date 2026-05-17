# mp-article-writor

[中文](#chinese) | [English](#english)

---

<a id="english"></a>

A Claude Code Skill that helps content creators craft long-form articles for WeChat Official Accounts (公众号) and SSPAI-style platforms. Covers a complete 9-step writing workflow from intent understanding to final draft.

## Features

- **9-step writing workflow**: Intent understanding → Style calibration → Outline design → Draft writing → Independent review → Fact-checking → Revision → Final self-check → Finished article
- **Independent review + fact-checking**: Subagent-powered reviews that detect AI-generated tone, logical gaps, structural symmetry, and factual accuracy
- **"Human voice" final check**: Evaluates whether the article reads like "a knowledgeable friend chatting" or "AI outputting information"
- **Style calibration**: Dual reference system (essay style analysis + writing style guide) to match your voice
- **Self-check checklist**: Four-layer quality gate — hard rules, style consistency, HKR scoring, human voice check

## Installation

### Via Claude Code Marketplace

In Claude Code:
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

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

The Skill follows a strict 9-step workflow, completing each step before moving to the next.

## Workflow

```
Step 1  Understand intent     → Confirm angle, depth, theme, materials
Step 2  Read references        → Calibrate voice (essay analysis + style guide)
Step 3  Design outline & style → Present outline, await confirmation
Step 4  Write first draft      → Follow all writing rules
Step 5  Independent review     → AI-tone detection, logic, structure, information density
Step 6  Fact-checking          → Data sources, scene authenticity, terminology accuracy
Step 7  Revise draft           → Address feedback item by item
Step 8  Final self-check       → Four-layer quality checklist
Step 9  Finalize               → Update file + self-check report + title suggestions
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

一个 Claude Code Skill，帮助自媒体创作者将素材整理为公众号长文。覆盖从意图理解、大纲设计、初稿撰写到审读自检的完整写作工作流。

## 功能特性

- **9 步写作工作流**：意图理解 → 风格校准 → 大纲设计 → 初稿撰写 → 独立审读 → 事实核查 → 修改 → 终审自检 → 完成终稿
- **独立审读 + 事实核查**：通过 subagent 对初稿进行 AI 味检测、逻辑连贯性检查、事实性核查
- **「活人感」终审**：判断文章读起来是「朋友在聊天」还是「AI 在输出」
- **风格校准**：范文分析 + 行文风格指南双重校准
- **自检清单**：硬性规则、风格一致性、HKR 质检、活人感四层检查

## 安装

### 通过 Claude Code Marketplace

在 Claude Code 中运行：
```
/plugin marketplace add balabalabalading/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

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

Skill 会按 9 步工作流依次执行。

## 工作流

```
Step 1  理解作者意图    → 确认切入角度、深度、主旨、素材
Step 2  阅读参考资料    → 校准语感（范文分析 + 风格指南）
Step 3  设计大纲和风格  → 呈现大纲，等待确认
Step 4  编写初稿        → 按规则写作
Step 5  独立审读        → AI 味检测、逻辑、结构、信息密度
Step 6  事实核查        → 数据来源、场景真实性、术语拼写
Step 7  修改初稿        → 逐条处理反馈
Step 8  终审自检        → 四层自检清单
Step 9  完成终稿        → 更新文件 + 自检报告 + 标题推荐
```

## 自定义配置

安装后修改 `SKILL.md` 中的以下内容：
- **公众号名称**、**固定结尾**、**作者声音**、**读者画像**、**文件保存路径**
- 将 `references/范文风格分析.md` 替换为你自己的风格分析

## 相关文章

[AI + Skill，能够让生成的文章去除 AI 味吗？](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ)

## 许可证

[MIT](../LICENSE)

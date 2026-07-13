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
- **Two illustration styles**: Choose Guizang social-card layouts or Guizang material illustrations during intake; the WeChat composite cover always uses the social-card skill
- **Local-first image delivery**: Produces one 3.35:1 composite WeChat cover, body illustrations, editable files, prompts, and relative Markdown image links by default; PicGo upload is optional
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

The repository default branch is `main`. Existing clones that still track `master` should migrate before the remote branch is removed:

```bash
git fetch origin
git switch main
git branch --set-upstream-to=origin/main main
```

### Local testing

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

## Image publishing modes

Image publishing defaults to `local`. This mode generates all images and uses relative Markdown paths such as:

```markdown
![Diagram](article-assets/my-article/illustrations/V01-diagram.png)
```

The article remains complete and editable without PicGo. Upload the local images manually in the WeChat editor when publishing.

Set `MP_ARTICLE_IMAGE_MODE=picgo` to enable automatic upload. This is an explicit persistent authorization for the workflow to send final images to the PicGo Server. PicGo Desktop 2.2+ and PicGo Core Server 2.0+ are supported. Configure Tencent Cloud COS, GitHub, Alibaba Cloud OSS, or another image host inside PicGo; the skill never reads those credentials.

Requirements for PicGo mode:

- Node.js 18 or newer.
- A running PicGo Server. The default address is `http://127.0.0.1:36677`.
- Final image URLs must use HTTPS so the WeChat editor can load them publicly.

Environment variables:

```text
MP_ARTICLE_IMAGE_MODE=picgo
PICGO_SERVER_URL=http://127.0.0.1:36677
PICGO_SERVER_SECRET=<optional shared secret>
PICGO_REQUEST_TIMEOUT_MS=10000
```

`PICGO_SERVER_URL` accepts either a base address or a full `/upload` URL. You can also override it per command:

```bash
node scripts/upload-images-to-picgo.mjs \
  --article-title "My article" \
  --endpoint "http://127.0.0.1:36677/upload" \
  --file "cover=/absolute/path/to/cover.png" \
  --file "body-01=/absolute/path/to/V01.png"
```

Use `--dry-run` to inspect filenames and endpoints without contacting PicGo. If the server uses a shared secret, pass it only through `PICGO_SERVER_SECRET`; it is sent as a Bearer token and never printed.

Common failures:

- Connection failure: start PicGo Server and verify the host and port.
- Timeout: increase `PICGO_REQUEST_TIMEOUT_MS` or check the selected image host.
- HTTP 401: set the matching `PICGO_SERVER_SECRET`.
- Non-HTTPS result: configure PicGo to return a public HTTPS URL before replacing article links.

If PicGo is unavailable in explicit `picgo` mode, local files and relative links are preserved. The delivery report marks image publishing as pending and includes the retry command.

### Without PicGo

PicGo is not required. Keep the default `local` mode and the skill will still generate the article, composite cover, body illustrations, editable files, and relative Markdown image links. Upload those local images manually in the WeChat editor when publishing.

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
Step 10 Produce visuals        → Composite cover + body illustrations + local links or optional PicGo upload
Step 11 Delivery check         → Dimensions, image-publishing status, labels, data, permissions, and static-only outputs
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
- **本地优先的图片交付**：默认生成一张 3.35:1 组合封面、正文插图、可编辑文件、提示词和相对 Markdown 图片链接，可选择使用 PicGo 上传
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

仓库默认分支已经切换为 `main`。已有本地副本如果仍跟踪 `master`，请在远程分支清理前执行：

```bash
git fetch origin
git switch main
git branch --set-upstream-to=origin/main main
```

### 本地测试

```bash
/plugin marketplace add ./path/to/huuuuuuho-skills
/plugin install mp-article-writor@huuuuuuho
```

## 图片发布模式

图片发布默认使用 `local`。该模式生成全部图片，并在文章中使用相对 Markdown 路径，例如：

```markdown
![关系图](article-assets/my-article/illustrations/V01-关系图.png)
```

没有安装 PicGo 时，文章和图片仍然正常生成并保持可编辑。正式发布公众号时，在公众号编辑器中手动上传这些本地图片。

设置 `MP_ARTICLE_IMAGE_MODE=picgo` 后启用自动上传。这个设置代表用户对工作流的持久上传授权。支持 PicGo Desktop 2.2+ 和 PicGo Core Server 2.0+。腾讯云 COS、GitHub、阿里云 OSS 等具体图床均在 PicGo 内配置，Skill 不读取这些图床的凭据。

PicGo 模式要求：

- Node.js 18 或更高版本。
- PicGo Server 正在运行，默认地址为 `http://127.0.0.1:36677`。
- 最终图片地址使用 HTTPS，确保公众号编辑器可以公开加载。

环境变量：

```text
MP_ARTICLE_IMAGE_MODE=picgo
PICGO_SERVER_URL=http://127.0.0.1:36677
PICGO_SERVER_SECRET=<可选的 shared secret>
PICGO_REQUEST_TIMEOUT_MS=10000
```

`PICGO_SERVER_URL` 可以填写基础地址，也可以填写完整的 `/upload` 地址。单次运行可以通过命令覆盖：

```bash
node scripts/upload-images-to-picgo.mjs \
  --article-title "文章标题" \
  --endpoint "http://127.0.0.1:36677/upload" \
  --file "封面=/绝对路径/cover.png" \
  --file "正文01=/绝对路径/V01.png"
```

添加 `--dry-run` 可以检查文件名和服务地址，不会访问 PicGo。服务启用 shared secret 时，只通过 `PICGO_SERVER_SECRET` 提供；脚本使用 Bearer 请求头发送，不会打印该值。

常见问题：

- 连接失败，启动 PicGo Server，并检查主机和端口。
- 请求超时，增加 `PICGO_REQUEST_TIMEOUT_MS`，或检查当前图床服务。
- HTTP 401，设置与 PicGo Server 一致的 `PICGO_SERVER_SECRET`。
- 返回非 HTTPS 地址，先在 PicGo 中配置公开 HTTPS 域名，再替换文章链接。

显式使用 `picgo` 模式但服务不可用时，本地文件和相对路径会保留。交付报告将图片发布标记为待完成，并提供重新执行命令。

### 没有 PicGo

PicGo 不是必需依赖。保持默认的 `local` 模式，Skill 仍会生成文章、组合封面、正文插图、可编辑文件和相对 Markdown 图片链接。正式发布时，在公众号编辑器中手动上传这些本地图片。

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
Step 10 生产静态视觉    → 组合封面 + 正文插图 + 本地链接或可选 PicGo 上传
Step 11 交付检查        → 尺寸、图片发布状态、标签、数据、授权和静态输出
```

## 自定义配置

安装后修改 `SKILL.md` 中的以下内容：
- **公众号名称**、**固定结尾**、**作者声音**、**读者画像**、**文件保存路径**
- 将 `references/范文风格分析.md` 替换为你自己的风格分析

## 相关文章

[AI + Skill，能够让生成的文章去除 AI 味吗？](https://mp.weixin.qq.com/s/ayye6aaSlxAwf7gFjPHsRQ)

## 许可证

[MIT](../LICENSE)

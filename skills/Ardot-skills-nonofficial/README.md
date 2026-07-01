# Ardot Skills (非官方)

> Ardot MCP 工具的非官方 Skills 集合，参照 [Figma MCP Skills](../../../mcp-server-guide/skills/) 架构设计，基于 [Ardot-MCP-使用经验.md](../../../Ardot-MCP-使用经验.md) 中的实践经验编写。

## 设计理念

Ardot MCP 提供 17 个远程 API 工具用于创建和编辑设计文件。但这些工具本身只是原子操作 —— Agent 直接调用它们会遇到已知陷阱（颜色范围错误、变量绑定失效、TEXT 节点约束等）。

这些 Skills 充当 **MCP 工具的"使用说明书"**，在 Agent 调用 MCP 工具前注入领域知识，确保 Agent 像 Ardot 专家一样正确编排工具调用。

## 架构总览

```
┌────────────────────────────────────────────┐
│  ardot-generate-design  ardot-generate-library │  ← 高级工作流
│  ardot-style-guide                               │
└───────────────────┬────────────────────────┘
                    │ 依赖
┌───────────────────▼────────────────────────┐
│  ardot-use          ardot-create-new-file     │  ← 核心前提
│  (batch_edit DSL)   (create_new_page)         │
└────────────────────────────────────────────┘
                    │ 上下文注入
                    ▼
┌────────────────────────────────────────────┐
│  Ardot MCP Tools (17 个远程 API)              │  ← 执行引擎
└────────────────────────────────────────────┘
```

## 5 个 Skills 简介

| Skill | 角色 | 绑定工具 | 强制前提 |
|-------|------|---------|---------|
| **ardot-use** | 核心基类：batch_edit DSL 规则、8 个坑点、变量绑定、验证恢复 | `batch_edit` | 是 — 所有写操作 |
| **ardot-create-new-file** | 页面创建前提 | `create_new_page` | 是 |
| **ardot-style-guide** | 样式指南搜索与构建（Ardot 独有） | `search_style_guide`, `build_style_guide` | 否 |
| **ardot-generate-design** | 6 步完整页面构建工作流 | 编排多工具 | 否 |
| **ardot-generate-library** | 组件库/设计系统 3 阶段构建 | 编排多工具 | 否 |

## 依赖关系

```
ardot-generate-design ──→ ardot-use + ardot-create-new-file + ardot-style-guide
ardot-generate-library ─→ ardot-use + ardot-create-new-file
ardot-style-guide ──→ 无（独立）
ardot-create-new-file ─→ 无（独立）
ardot-use ──→ 无（但被其他 4 个依赖）
```

## 覆盖的已知坑点

来自 `Ardot-MCP-使用经验.md` 的 8 个坑点全部编码到 `ardot-use/references/gotchas.md`：

1. `updated: {}` 不代表失败
2. 绑定名每次 batch_edit 后失效
3. cornerRadius 变量绑定不生效
4. TEXT 在 I() 中不能直接绑定变量
5. variableModes 不可靠
6. 跨页写入需指定 pageId
7. batch_read 无法发现所有页面 ID
8. M() 目标父节点和 index 必须有效

## 参照来源

- Figma MCP Skills 架构：`mcp-server-guide/skills/`（8 个 skills，两层架构模型）
- Ardot 使用经验：`Ardot-MCP-使用经验.md`（工具清单、DSL 详解、8 个坑点）
- 架构分析文档：`figma-skills-mcp-analysis.md`

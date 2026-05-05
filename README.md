# wechat_official_account

本项目用于 Agent 辅助微信公众号创作，目标是把「写作整理、图片插入、隐私检查、语言修订、公众号排版、预览和草稿上传」这些步骤沉淀成可复用的 Agent 工作流。

项目目前包含两个 skill：

- `weekly-official-account-post`：用于整理中文周总结，生成真实 Markdown 文件，并通过分步骤审批完成隐私检查、语言纠正和文艺化润色。
- `md2wechat`：用于把 Markdown 转换为微信公众号可用的 HTML，生成本地预览，并在用户明确要求时上传图片或创建公众号草稿。

## 项目结构

```text
.
├── .codex/
│   └── skills/
│       └── weekly-official-account-post/
│           ├── SKILL.md
│           └── agents/
│               └── openai.yaml
├── .agents/
│   └── skills/
│       └── md2wechat/
│           └── SKILL.md
├── themes/
│   └── ocean-calm-safe.yaml
├── tools/
│   ├── generate_ocean_preview.py
│   └── upload_ocean_preview_images.py
├── skills-lock.json
└── README.md
```

`articles/` 目录用于存放文章草稿、图片、预览 HTML、草稿 JSON 等创作产物，默认被 Git 忽略，避免把个人内容和素材误提交到仓库。

## weekly-official-account-post

这是一个用于整理微信公众号周总结的 skill。它会把用户提供的随笔原文和沙箱中的图片整理成真实的 Markdown 文件，并通过分步骤审批完成隐私检查、语言纠正和语言润色。

### 包含文件

- `.codex\skills\weekly-official-account-post\SKILL.md`  
  skill 的核心说明文件，定义具体工作流程、格式规则、图片处理方式、隐私核查、语言纠正和润色审批规则。

- `.codex\skills\weekly-official-account-post\agents\openai.yaml`  
  Codex App 的界面元数据文件，用于控制 `/` 菜单中的显示名称、简短说明和默认提示词。它不负责具体执行逻辑。

### 主要功能

1. **生成真实 Markdown 文件**  
   在沙箱中创建并持续更新实际的 `.md` 文件，而不是只在对话中给出草稿。

2. **自动查找并插入图片**  
   第一步会自动扫描当前 workspace 中的图片文件，根据**文件名、时间、路径和图片内容**判断插入位置。

3. **公众号格式整理**  
   保留原文小标题顺序，将小标题转换为 `PART x` 格式，并按要求为特定章节的段落添加编号。

4. **自动修正标点**  
   自动处理缺少句号、中英文标点混用、重复标点、标点前后空格等问题。

5. **隐私核查**  
   单独列出可能导致隐私泄露的内容，等待用户选择要删除或遮蔽的项目后，再修改 Markdown 文件。

6. **语言纠正**  
   列出明显表达错误、不通顺或有语病的句子，等待用户审批后再写入文件。

7. **文艺化润色与表达审查**  
   在保持原意的基础上，提出更有散文气息的润色建议；同时指出不成熟、不妥当、可能不适合公开发布的表达。

8. **分步审批**  
   每一步都必须等用户明确表示可以进入下一步后才继续，每一步都可以经历多轮修改。

### 使用方法

1. 把本周原文、图片和截图放入当前 workspace，推荐放在 `articles/<日期或标题>/` 下。
2. 在 Codex 中说明要使用 `weekly-official-account-post` 整理周总结，并提供文章标题、原文内容和期望输出路径。
3. Agent 会先创建真实 `.md` 文件，并自动插入可匹配的图片。
4. 你检查第一版 Markdown 后，明确回复“可以进入下一步”，Agent 才会进入隐私核查。
5. 隐私核查、语言纠正、文艺化润色都会先列出编号建议，只有你批准的编号才会写入文件。
6. 最终得到一份可继续交给 `md2wechat` 转换和预览的 Markdown 文件。

适合的输入方式示例：

```text
使用 weekly-official-account-post，帮我整理《2026 夏一周总结》。
原文如下：……
```

## md2wechat

`md2wechat` 基于 GitHub 高 stars 项目 `geekjourneyx/md2wechat-skill` 开发，用于处理微信公众号文章的转换、预览、图片上传和草稿创建流程。

本项目中的 `md2wechat` skill 在原版基础上做了面向 Codex / Claude Code 和本地安全工作流的调整。

### 包含文件

- `.agents\skills\md2wechat\SKILL.md`  
  Agent 使用的 `md2wechat` skill 说明文件，定义 CLI 解析、数据传输边界、本地优先主题转换、元数据规则、预览规则和草稿创建流程。

- `themes\ocean-calm-safe.yaml`  
  面向微信公众号文章的主题配置。当前配套本地生成脚本使用，强调安全内联样式、明确颜色和微信兼容性。

- `tools\generate_ocean_preview.py`  
  本地 HTML 预览生成脚本。用于在不调用远程 AI 的情况下，把 Markdown 转换成符合 `ocean-calm-safe` 风格的预览 HTML。

- `tools\upload_ocean_preview_images.py`  
  本地 HTML 推送草稿前的图片处理脚本。用于上传本地图片、替换 HTML 中的本地图片路径，并生成创建草稿所需的中间数据。

- `skills-lock.json`  
  skill 锁文件，记录 `md2wechat` skill 的来源、路径和内容哈希，便于复现和校验。

### 安装 skill

环境配置见原仓库“快速开始”部分。配置完后，终端里应该能直接运行：

```bash
md2wechat --help
```

可用下面的命令查看账号登录状态和配置是否有效：

```bash
md2wechat config validate
```

对于 Codex，可以在沙盒中执行：

```bash
npx skills add https://github.com/geekjourneyx/md2wechat-skill --skill md2wechat -a codex
```

这会安装原版 skill。也可以不安装原版 skill，直接使用本项目维护的 `SKILL.md`。本项目版本的主要调整包括：

- 加了 CLI Resolution：优先 `md2wechat`，Windows 下 fallback 到 `%APPDATA%\npm\md2wechat.cmd`，避免 `md2wechat.ps1` 被 PowerShell execution policy 拦住。
- 加了 Data Transfer Boundaries：区分本地预览、AI/API 转换、上传图片、创建草稿/图文帖这些不同风险动作。
- 删除了原文件里的中文和乱码段落，整份文件现在无中文、无非 ASCII 字符。
- AI 主题默认本地优先，不调用远程 AI；先查本地脚本，验证是否匹配主题要求；正确就直接用，不存在或不正确就先生成/修正脚本。
- 摘要优先读 metadata；没有可用摘要时，每次根据文章实际内容生成，不使用固定范式，不编造内容，并保持在限制内。
- 明确本地 HTML 推送草稿箱的流程：上传图片、替换本地图片链接、确认无本地路径、使用上传图片的 `media_id` 做封面、生成无 BOM 的 draft JSON，再调用 `create_draft`。

### 使用方法

与原项目调用外部 API 不同，我的做法是由 Codex 全权负责所有任务。比如：

```text
帮我把 2026夏一周总结.md 转换成公众号推文。使用 ocean-calm-safe 风格。生成预览结果给我看。
```

```text
推送到草稿箱。
```

你也可以让 Agent 创建、修改风格。`ocean-calm-safe` 风格就是我基于 `ocean-calm` 风格修改的，更稳定，在深色模式下有更好的表现。
# AGENTS.md

> 本文件给 Codex 等其他 agent 用，与 `CLAUDE.md` 保持同一套口径。**规则单一来源在 `.claude/docs/` 各主题文件**——开工前先读对应文件，本文件只做索引 + 内联最关键的几条，两边冲突时以 `.claude/docs/` 为准。

## 规则索引（单一来源，按需阅读）

- 这个仓库是什么 / 署名归位规则 → `.claude/docs/repo-overview.md`
- 统一人物底座（视觉 IP） → `.claude/docs/character-base.md`
- 常用命令 → `.claude/docs/commands.md`
- Skills 同步 → `.claude/docs/skills-sync.md`
- 抖音转写（链接 → mp4 + 文字） → `.claude/docs/douyin-transcribe.md`
- 视频流水线（文章 → mp4，script.md 约定） → `.claude/docs/video-pipeline.md`
- 语言 → `.claude/docs/language.md`

## 必须不能错的几条（内联）

- **双平台**：本工作区在 **macOS 和 Windows 两台机器**上都会用（git 同步）。所有命令、路径、文档说明都要双平台兼容（venv 是 `bin/python` vs `Scripts/python.exe`；skills 同步 macOS 走 symlink、Windows 手动 copy；GBK/代理坑是 Windows 特有）。
- **署名归位**：转写 / 搬运别人的视频做成本仓库成品时，结尾 CTA、署名、品牌一律换成「AI少年」，**别保留原作者**。
- **人物底座**：所有产物的封面 / 配图 / IP 形象统一用 `character/persona-clay-v5.png`（设定见 `character/persona.md`）。三个辨识锚点每次出图必保留：黑色细框矩形眼镜 / 珊瑚橘短袖 / 笔记本上的发光白色 Apple 图标。旧图（紫色连帽衫等）仅是历史存档。
- **语言**：仓库内容、口播稿、新增注释一律简体中文。
- **真实底线**：经历、数字、踩坑细节不编；材料里没有的命令细节 / 数字 / 论断不要自行添加，留 `> [!待补]` 占位问用户。

## 仓库结构（概要，详见 repo-overview.md）

内容创作工作区，不是单一应用。仓库根下**一个选题一个项目目录**（抖音来源用「作者-标题前20字」命名，自拟选题用描述性短名），产物多为纯静态 HTML deck，部分含转写 txt / 口播稿 script.md / 成片 mp4。公共资产：`character/`（人物底座）、`archive/`（归档）。skills 在 `.agents/skills/` 与 `.claude/skills/`，当 vendor 内容对待，除非明确在更新 skill。

本仓库**是 git 仓库**（remote：`github.com/aehyok/douyin`，主分支 `master`）。

## 开发与校验约定

- 没有统一构建/测试工具链：deck 直接用浏览器打开对应目录 `index.html`（← → / 空格 / 点击翻页）。
- 改版 deck 用递增目录名（如 `deck_v4/`），**不要覆盖旧版本**，除非用户明确要求。
- 没有自动化测试，校验是视觉的：打开改动的 `index.html` → 检查键盘/点击翻页 → 逐页截图 → 确认无文字溢出、缺资源、中文乱码。截图存到该 deck 的 `preview/` 或 `_preview/`。
- 中文展示文字放 HTML 里叠字（imgen 生成的底图不负责渲染准确中文），沿用粘土风样式与 1920x1080 页面尺寸。

## 提交约定

- Conventional Commit 中文风格短前缀：`feat:` / `chore:` / `docs:` / `fix:`。
- PR 写清改了哪些目录、附视觉改动的截图或 preview 路径，注明旧 deck 是保留还是有意替换。

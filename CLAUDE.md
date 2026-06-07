# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 这个仓库是什么

这是「AI 少年」的**内容创作工作区**（面向抖音 / B 站 / 视频号的 AI 科普内容），不是单一应用。它由几个相互独立的产物 + 安装好的 skills 组成：

- `ai-agent-video/` — 一期视频项目。`article.md`/`script.md`/`outline.md` 是内容三件套，`presentation/` 是把口播稿做成「看起来像视频」的网页（Vite + React + TS）。由 `web-video-presentation` skill 脚手架产出。
- `deck/` — 独立的全屏图文 HTML 演示稿（粘土风，10 页，主题「Codex 接入国产模型」），纯静态 HTML/CSS，由 `visual-deck-main` skill 产出。与 `ai-agent-video` **无代码关联**。
- `garden-skills-main/` — clone 的 garden skills 源码仓库（skills 的来源），一般只读。
- `kb-retriever-1.0.0/` — 知识库检索 skill 的打包目录。
- `.agents/skills/` 与 `.claude/skills/` — 安装的 skills。⚠️ 见下方「Skills 同步」。

整个仓库**不是 git 仓库**（`git rev-parse` 失败）。

## 统一人物底座（视觉 IP）

`deck/character/` 是整个工作区的**统一人物底座**——所有产物（`deck/`、`ai-agent-video/` 等）的封面 / 视觉页 / 口播配图 / IP 形象都用这一个，保持形象一致、不要各做各的。

- 设定文档：`deck/character/persona.md`（外形 / 服装 / 粘土风规格 / imgen 主体描述槽位）
- 当前主形象：`persona-clay-v2.png`（东亚青年男 + 黑框矩形眼镜 + 珊瑚橘短袖 + 笔记本印 Apple 图标，3D 粘土定格风），配薰衣草紫背景
- 备份：`persona-clay.png`（早期藏青连帽版）
- **三个辨识锚点每次出图必保留**：黑色细框矩形眼镜 / 珊瑚橘短袖 / 笔记本上的发光白色 Apple 图标
- 出人物图优先 img2img 引用 `persona-clay-v2.png`；纯 prompt 用 `persona.md` 第六节的「主体片段」。出图**不要透明背景**（imgen 后端不支持）。

## 常用命令

真正有构建/测试工具链的只有 `ai-agent-video/presentation/`（先 `cd` 进去）：

```bash
npm run dev                  # Vite 开发服务器
npm run build                # tsc -b 类型检查 + vite build
npm run lint                 # eslint .
npm run preview              # 预览 dist

npm run extract-narrations   # 扫所有 narrations.ts → audio-segments.json
npm run extract-narrations -- --print
npm run synthesize-audio     # 按 audio-segments.json 逐段合成 public/audio/<id>/<N>.mp3
npm run synthesize-audio -- --force                  # 强制重新合成
PRESENTATION_TTS=openai npm run synthesize-audio      # 切 TTS provider（默认 minimax）
npm run synthesize-audio -- --provider=elevenlabs --voice=Rachel
```

`deck/` 是纯静态，直接用浏览器打开 `deck/index.html` 即可（← → / 空格 / 点击翻页）。截图预览走 `visual-deck-main` skill 的 `preview.sh`（Windows 上的坑见全局 memory `preview-sh-windows-fix.md`）。

测试：本仓库目前**没有测试套件**。`verify-step-*.png` 是用 puppeteer-core 截图做的人工校验产物，不是自动化测试。

## presentation 应用架构（关键）

这是一个**点击驱动、伪装成视频**的 16:9 网页：每次点击 / 空格推进口播稿的一个「节拍（step）」，每个 step 独占整屏。架构核心是**单一真相源**约束：

- **`src/chapters/<NN>-<id>/narrations.ts`** 导出 `narrations: Narration[]`，是 step 数和口播文本的**唯一真相源**。数组长度 = 该章 step 数。
- 章节组件 `<Chapter>.tsx` 用 `if (step === N)` 分支渲染每个 step。出现的最大 `N` + 1 **必须等于** `narrations.length`，否则会漂。
- `src/registry/chapters.ts` 按演示顺序登记每个 `ChapterDef`（`id` / `title` / `narrations` / `Component`）。**新增章节就改这里。**
- `Narration` 是 `string`；空串 `""` 表示该 step 无音频（静默转场），Auto 模式回退到按字数估算的时长（≈250ms/字，见 `App.tsx` 的 `estimateMs`）。

数据流（5 处必须对齐：script / outline / 章节代码 / chapters.ts / 音频文件）：

```
narrations.ts ──extract-narrations.ts──▶ audio-segments.json ──synthesize-audio.sh──▶ public/audio/<id>/<N>.mp3
                                                                       │ 加载 tts-providers/<name>.sh 适配器
App.tsx 按约定取音频：/audio/<chapter-id>/<step+1>.mp3（文件名 1-indexed）
```

运行时关键模块：
- `hooks/useStepper.ts` — 游标 `{chapter, step}`，键盘导航（←→/空格/Home/End/数字跳章），cursor 持久化到 localStorage（`STORAGE_KEY` 带版本号，结构变更时要 bump）。
- `hooks/useAudioPlayer.ts` / `useAutoMode.ts` — Auto 模式靠 `audio.ended` 自动推进，音频缺失才用估算时长兜底。
- `components/Stage.tsx` + `hooks/useStageScale.ts` — 把固定尺寸舞台等比缩放铺满视口。

**主题系统**：颜色 / 字体全部来自 `src/styles/tokens.css`（当前激活主题，由脚手架生成）。章节代码**绝不硬编码**调色板 / 字体名 —— 视觉只走 CSS token。详见 skill 的 `references/THEMES.md`。

**TTS provider 适配器**：`scripts/tts-providers/<name>.sh` 必须实现 `tts_synthesize <text> <out> [voice]`（必需）、可选 `tts_check` / `tts_install_help`。内置 `minimax.sh`（默认）和 `openai.sh`。新增 provider 见 `tts-providers/README.md`。合成需要本机有 `jq`。

## Skills 同步（重要）

本机用户全局规则：`npx skills` 会把 skill 装到 `.agents/skills/`，但 Claude Code 实际读 `.claude/skills/`。Windows symlink 不可靠，所以 **add / update / remove skill 后要手动把 `.agents/skills/` 同步到 `.claude/skills/`**（项目级）。详见 `~/.claude/skills-sync.md`。

> macOS 上 `npx skills add` 会自动建好 `.claude/skills/<name>` → `../../.agents/skills/<name>` 的 symlink、Claude Code 直接读到，**无需手动 copy**（手动同步主要是 Windows 的坑）。装 hyperframes 时即如此。

## 视频流水线（文章 → mp4）

把一篇文章做成成片视频的**完整闭环**，由两个 skill 接力（已在本机验证可跑，2026-06）：

```
文章
 └─[visual-deck]→ 逐页大纲 → imgen 底图+HTML 叠字 / 信息页纯 HTML → 合成 deck → 截图校验
       └─[hyperframes]→ 迁成 composition + 加可 seek 动画 → npx hyperframes render → MP4
```

- **前半段（visual-deck）**：见上文，产物是可翻页静态 HTML deck。
- **后半段（hyperframes）**：HeyGen 的 hyperframes（`npx skills add heygen-com/hyperframes` 装的一套 skill：`hyperframes` 主体 + `hyperframes-cli`/`-media`/`-registry` + gsap/animejs/css-animations/waapi/lottie/three/typegpu/tailwind 适配器 + website-to-hyperframes 等）。把带动画的 HTML composition **逐帧渲染成确定性 MP4**。
  - 命令：`npx hyperframes init <dir>` 脚手架 → `npx hyperframes render` 出 mp4（也有 `preview` / `lint` / `doctor`）。
  - 配音字幕：`hyperframes-media` 做 TTS（Kokoro）+ Whisper 自动字幕 + 抠背景，首次跑会下模型。
  - 本机环境：Node 22 / FFmpeg / system Chrome 即可；**Docker 是可选的**（容器化渲染才用，没装不影响本地 render）。

**两个接缝坑（动手前必读）**：
1. visual-deck 的 `deck.html` 骨架与 hyperframes 是**两套播放/动画机制**——中间页要**迁成 hyperframes composition**（纯 HTML、无 build）才能 render，别直接拿 deck.html 去渲染。
2. hyperframes 逐帧渲染要求动画**可 seek**（GSAP timeline / WAAPI `currentTime` / CSS animation-delay 这类）；实时或随机动画逐帧会飘。

## 语言

仓库内容与口播稿均为简体中文，新增内容 / 注释保持中文一致。

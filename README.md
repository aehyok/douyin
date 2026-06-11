# 🎬 AI少年 · 内容创作工作区

> 面向抖音 / B 站 / 视频号的 **AI 科普短视频**内容创作工作区。  
> 从选题拆解 → 口播稿 → 图文演示稿 → 成片 MP4，全流程 AI 辅助创作。

<p align="center">
  <img src="character/persona-clay-v5.png" width="280" alt="AI少年 — 粘土风 IP 形象" />
</p>

<p align="center">
  <b>大家好，我是 AI少年 👋</b><br/>
  AI 的事，听 AI少年 说
</p>

---

## 📖 项目简介

这**不是**一个单一应用，而是一个**内容创作工作区**——仓库根目录下，每个选题一个独立项目目录，产物主要为：

- 📝 **口播稿**（`script.md`）— 内容流水线的单一来源
- 🖼️ **图文演示稿**（HTML Deck）— 全屏可翻页的静态 HTML，imgen 底图 + HTML 叠中文
- 🎥 **成片视频**（MP4）— 通过 HyperFrames 逐帧渲染的最终产物
- 📄 **转写文本**（`transcript.md`）— 抖音 / B 站视频的转写毛坯

## 📂 目录结构

```
AISpark_douyin/
│
├── character/                    # 🎨 统一人物底座（视觉 IP）
│   ├── persona.md                #    人物设定文档
│   ├── persona-clay-v5.png       #    当前主形象（珊瑚橘短袖 + 橙色耳机）
│   ├── persona-clay-v2.png       #    早期版本备份
│   └── persona-clay.png          #    早期藏青连帽版备份
│
├── deck/                         # 自拟选题 — AI Agent 科普 deck
├── stepfun-deck/                 # 自拟选题 — StepFun 阶跃星辰 deck
├── codex-skills-deck/            # 自拟选题 — Codex Skills deck
├── claude-code-deepseek/         # 自拟选题 — Claude Code + DeepSeek（多版本迭代）
├── douyin-codex-hyperframes/     # 自拟选题 — Codex HyperFrames 转写
├── douyin-claude-code-config/    # 自拟选题 — Claude Code 配置教程
│
├── 小墨同学-Codex强的根本不是…/    # 抖音转写 — 小墨同学的视频二创
├── 雨哥聊AI-撞限别干等…/          # 抖音转写 — 雨哥聊AI的视频二创（含成片）
│
├── archive/                      # 📦 已归档的旧产物
├── .agents/skills/               # 🔧 已安装的 Agent Skills
├── .claude/                      # 🤖 Claude 配置与文档
│
├── AGENTS.md                     # Agent 协作规则索引
├── CLAUDE.md                     # Claude 项目规则
├── .gitignore
└── README.md                     # 👈 你在这里
```

### 选题目录命名规则

| 来源 | 命名规则 | 示例 |
|---|---|---|
| 抖音转写 | `作者名-标题前20字` | `雨哥聊AI-撞限别干等!一个设置让 Codex 额度` |
| 自拟选题 | 描述性短名 | `claude-code-deepseek`、`stepfun-deck` |

### 成片项目目录结构（参考）

以 `雨哥聊AI-撞限别干等…/` 为最完整的参考：

```
<选题目录>/
├── script.md             # 口播稿（AI少年口播版，流水线起点）
├── transcript.md         # 转写毛坯（来自抖音原视频）
├── <视频ID>.mp4          # 原视频文件
├── <视频ID>.txt          # 原视频字幕
├── deck/                 # 图文演示稿（HTML Deck）
│   ├── index.html
│   └── assets/
├── video/                # HyperFrames composition
├── build_tts.py          # TTS 配音构建脚本
├── narration.wav         # 配音音频
├── manifest.json         # HyperFrames 清单
└── *-成片.mp4            # 🎬 最终成片
```

## 🎨 人物底座（视觉 IP）

所有产物的封面、配图、IP 形象统一使用同一人物底座，保持品牌一致性。

**三大辨识锚点（每次出图必保留）：**

| 锚点 | 描述 |
|---|---|
| 🤓 黑色细框矩形眼镜 | 标志性配饰，必须保留 |
| 🧡 珊瑚橘短袖 T 恤 | 当前主形象服装 |
| 💻 笔记本 Apple 发光图标 | 机盖朝镜头，发光白色 Apple Logo |

**视觉风格**：3D 粘土定格动画（claymation），柔和薰衣草紫背景，圆润可爱比例

> 详细设定见 [`character/persona.md`](character/persona.md)

## 🔧 创作流水线

```
文章 / 抖音转写
 └─① 口播稿 script.md（AI少年口播版，先产、先给用户过）
      └─② [visual-deck] → 逐页大纲 → imgen 底图 + HTML 叠字 → 合成 deck
           └─③ [hyperframes] → 迁成 composition + 动画 → render → MP4
                ↑ hyperframes-media: TTS 配音 + Whisper 字幕
```

### Step 0 · 口播稿 `script.md`

口播稿是整个流水线的**单一来源**，先产出、先过审，确认后才进后续环节。

- **固定开场**：先抛钩子 → 「大家好，我是 AI少年」
- **固定结尾**：「AI 的事，听 AI少年 说，关注我，咱们下期接着聊」
- **真实底线**：经历、数字、踩坑细节不编，材料没有的留 `> [!待补]` 占位

### Step 1 · 图文演示稿（Visual Deck）

使用 `visual-deck-main` skill，产出全屏可翻页的静态 HTML deck：

- 视觉页：imgen 生成粘土风底图 + HTML 叠准确中文文字
- 信息页：纯 HTML/CSS 结构化排版
- 页面尺寸：1920×1080，← → / 空格 / 点击翻页

### Step 2 · 成片视频（HyperFrames）

使用 HyperFrames 套件将 HTML composition 逐帧渲染为 MP4：

- `npx hyperframes init <dir>` — 脚手架
- `npx hyperframes render` — 渲染出片
- `npx hyperframes preview` / `lint` / `doctor` — 预览与调试

配音字幕由 `hyperframes-media` 完成（Kokoro TTS + Whisper 转写）。

## 🛠️ 技术栈

| 技术 | 用途 |
|---|---|
| **HTML / CSS / JS** | 静态 deck 与 HyperFrames composition |
| **HyperFrames** | HTML → 确定性 MP4 逐帧渲染 |
| **imgen** | AI 图片生成（粘土风底图） |
| **Kokoro TTS** | 文字转语音配音 |
| **Whisper** | 语音转文字（字幕生成） |
| **Node.js / FFmpeg** | 渲染环境依赖 |
| **Python** | TTS 脚本等辅助工具 |

## 🚀 快速开始

### 环境要求

- Node.js 22+
- FFmpeg（已加入 PATH）
- Chrome 浏览器（HyperFrames 渲染需要）
- Python 3.x（TTS 脚本可选）

### 查看演示稿

直接用浏览器打开任意选题目录下的 `index.html`：

```bash
# 例如查看 Claude Code + DeepSeek 最新版 deck
start claude-code-deepseek/deck_v8/index.html
```

**操作方式**：← → 方向键 / 空格 / 鼠标点击翻页

### 渲染视频（需安装 HyperFrames）

```bash
# 预览 composition
npx hyperframes preview <composition-dir>

# 渲染为 MP4
npx hyperframes render <composition-dir>
```

## 📝 署名规则

> ⚠️ **重要**：转写 / 搬运别人视频做成本仓库成品时，结尾 CTA、署名、品牌一律换成「**AI少年**」，不保留原作者。

## 📋 Git 提交约定

使用 Conventional Commit 中文风格：

```
feat: 新增选题/功能
fix: 修复问题
docs: 文档更新
chore: 杂项维护
```


## 待参考

```
- https://github.com/wechatpay-apiv3/wechatpay-skills
- https://github.com/tobemaster56/x-article-poster
- https://thariqs.github.io/cc-video-editing-deck/
```


## 📄 License

本仓库为个人内容创作工作区，仅供学习参考。

---

<p align="center">
  <b>AI 的事，听 AI少年 说 ✨</b><br/>
  关注我，咱们下期接着聊
</p>

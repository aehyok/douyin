## 视频流水线（文章 → mp4）

把一篇文章做成成片视频的**完整闭环**，由两个 skill 接力（已在本机验证可跑，2026-06）：

```
文章 / 抖音转写
 └─① 口播稿 script.md（AI少年口播版，先产、先给用户过）
      └─[visual-deck]→ 逐页大纲 → imgen 底图+HTML 叠字 / 信息页纯 HTML → 合成 deck → 截图校验
            └─[hyperframes]→ 迁成 composition + 加可 seek 动画 → npx hyperframes render → MP4
                  ↑ hyperframes-media 拿 script.md 做 TTS 配音 + Whisper 字幕
```

### 第 0 步 · 口播稿 `script.md`（单一来源，流水线起点）

口播词**不是任何 skill 自动生成的**——visual-deck 只产图文 HTML（大纲里没有口播字段）。所以每个成片项目目录都放一份 `script.md` 当**口播稿单一来源**：先产出、先让用户过，确认后才进出图和渲染。它一份文本同时驱动下游两件事：① 给 visual-deck 当「这页讲什么」的配图依据；② 给 `hyperframes-media` 做 TTS 配音 + Whisper 字幕。

- **存放位置**：仓库根的**成片项目目录**里，跟该选题的 `deck/`、`*.mp4`、`transcript.md` **同级** —— 即 `<仓库根>/<选题目录>/script.md`。选题目录沿用既有惯例：抖音来源用「作者-标题前20字」（见 `小墨同学-…/`、`雨哥聊AI-…/`），自拟选题用描述性短名（见 `douyin-codex-hyperframes/`、`stepfun-deck/`）。**不落在 skill 目录、不落 `downloads/`**。
- **完整样例（模板）**：`雨哥聊AI-撞限别干等…/` 是流水线全量产物的参考结构 —— `script.md`（口播稿）+ `transcript.md`（转写毛坯）+ 原视频 `<视频ID>.mp4`/`.txt` + `deck/`（图文稿）+ `video/`（hyperframes composition）+ `build_tts.py`/`narration.wav`（配音）+ `*-成片.mp4`（最终成片）。新建成片项目照这个结构来。
- **来源两条路**：给文章 → 我拆解后**写** script.md；给抖音链接 → `douyin-video-transcribe` 转写，毛坯落 `transcript.md`，我把整理润色后的「AI少年口播版」誊进 `script.md`（样例见 `雨哥聊AI-撞限别干等…/script.md` 与同目录 `transcript.md` 的对照）。
- **固定头尾（IP 一致，每条必带）**：开场先抛钩子再自报家门「**大家好，我是 AI少年**」；结尾固定「**AI 的事，听 AI少年 说，关注我，咱们下期接着聊**」。
- **结构约定**：
  ```markdown
  # <选题> — 口播稿
  - 来源 / 目标平台 / 时长目标 / 人物底座(persona-clay-v5.png)
  ## 口播正文（AI少年口播版，可直接念 / 喂 TTS）
     <钩子 → 自报家门 → 分段正文 → 固定尾>
  ## 分页对应（口播段 → deck 页 → 页类型）   ← 即 visual-deck 的逐页大纲，避免重复
  ```
- **真实底线**：经历、数字、踩坑细节不编；用户没给的留 `> [!待补]` 占位问用户（沿用 visual-deck 第1步的底线）。

- **前半段（visual-deck）**：见上文，产物是可翻页静态 HTML deck。
- **后半段（hyperframes）**：HeyGen 的 hyperframes（`npx skills add heygen-com/hyperframes` 装的一套 skill：`hyperframes` 主体 + `hyperframes-cli`/`-media`/`-registry` + gsap/animejs/css-animations/waapi/lottie/three/typegpu/tailwind 适配器 + website-to-hyperframes 等）。把带动画的 HTML composition **逐帧渲染成确定性 MP4**。
  - 命令：`npx hyperframes init <dir>` 脚手架 → `npx hyperframes render` 出 mp4（也有 `preview` / `lint` / `doctor`）。
  - 配音字幕：`hyperframes-media` 做 TTS（Kokoro）+ Whisper 自动字幕 + 抠背景，首次跑会下模型。
  - 本机环境：Node 22 / FFmpeg / system Chrome 即可；**Docker 是可选的**（容器化渲染才用，没装不影响本地 render）。

**两个接缝坑（动手前必读）**：
1. visual-deck 的 `deck.html` 骨架与 hyperframes 是**两套播放/动画机制**——中间页要**迁成 hyperframes composition**（纯 HTML、无 build）才能 render，别直接拿 deck.html 去渲染。
2. hyperframes 逐帧渲染要求动画**可 seek**（GSAP timeline / WAAPI `currentTime` / CSS animation-delay 这类）；实时或随机动画逐帧会飘。

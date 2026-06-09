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

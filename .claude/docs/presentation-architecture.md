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

## 这个仓库是什么

这是「AI 少年」的**内容创作工作区**（面向抖音 / B 站 / 视频号的 AI 科普内容），不是单一应用。**仓库主人 / 创作者本人就是「AI少年」**（git 提交用户名也是 `AI少年`）——这里产出的都是 AI少年 自己的内容。

> ⚠️ **署名归位规则**：转写 / 搬运别人的视频做成本仓库的成品时，结尾 CTA、署名、品牌一律换成「AI少年」，**别保留原作者**。例：转写「小墨同学」的抖音视频做 PPT，原口播结尾「关注小墨」，成品必须改成「关注 AI少年」（曾踩坑：`codex-skills-deck` 初版误留了「关注小墨」）。

它由几个相互独立的产物 + 安装好的 skills 组成：

- `ai-agent-video/` — 一期视频项目。`article.md`/`script.md`/`outline.md` 是内容三件套，`presentation/` 是把口播稿做成「看起来像视频」的网页（Vite + React + TS）。由 `web-video-presentation` skill 脚手架产出。
- `deck/` — 独立的全屏图文 HTML 演示稿（粘土风，10 页，主题「Codex 接入国产模型」），纯静态 HTML/CSS，由 `visual-deck-main` skill 产出。与 `ai-agent-video` **无代码关联**。
- `garden-skills-main/` — clone 的 garden skills 源码仓库（skills 的来源），一般只读。
- `kb-retriever-1.0.0/` — 知识库检索 skill 的打包目录。
- `.agents/skills/` 与 `.claude/skills/` — 安装的 skills。⚠️ 见「Skills 同步」。

整个仓库**不是 git 仓库**（`git rev-parse` 失败）。

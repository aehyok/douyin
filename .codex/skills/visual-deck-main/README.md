# visual-deck

> A Claude Code **skill** that turns a topic or outline into a multi-page, full-screen **HTML presentation deck** — mixing AI-generated visual backgrounds (`imgen`) with HTML-overlaid, pixel-accurate text.
>
> 把一个选题 / 大纲做成「图文混合的全屏 HTML 演示稿」——科普图、讲解 PPT、知识卡、口播配图、流程图解。

---

## 核心思路：图 + HTML 混合，不是纯图也不是纯 HTML

这是这个 skill 的判断基础——逐页判类型，各干各擅长的：

| 方式 | 质感 | 文字 | 问题 |
|---|---|---|---|
| 纯 imgen 整图 | ★★★ | ✕ 中文偶错、不能改 | 文字不可控 |
| 纯 HTML 复刻 | ★★ 打折 | ★★★ | 让 HTML 干它不擅长的「复刻 AI 整图质感」，差距大 |
| **图 + HTML 混合**（本 skill） | ★★★ | ★★★ | 各干各擅长的 |

- **imgen** 擅长整张渲染的质感（人物、3D 元素、场景光影浑然一体）→ 出**视觉页底图**
- **HTML** 擅长准确文字、排版、交互 → **叠准确中文字**、画**信息页**（波形 / 时间线 / 表格 / 代码 / 流程，imgen 画这些会糊）

→ 结论：**视觉页走「imgen 留白底图 + HTML 叠字」，信息页走「纯 HTML/CSS」。**

## 工作流（5 步）

```
选题 → 大纲(逐页规划 + 定每页类型) → 逐页做 → 合成翻页 → 截图预览
                                       ├─ 视觉页 → imgen 留白底图 + HTML 叠字(cover 铺满)
                                       └─ 信息页 → 纯 HTML/CSS(用组件库)
```

1. **选题 → 大纲**：逐页列「讲什么 / 屏上放什么 / 页类型（视觉页 or 信息页）」
2. **视觉页**：`imgen` 出主体在一侧、另一侧留白、无文字的底图 → HTML 用 `background:cover` 铺满 + `vw` 叠字
3. **信息页**：用 `assets/style-claymation.css` 组件库（卡片 / 波形 / 时间线 / 字幕表 / 终端 / 文件 / 标签云 / 步骤条）纯 HTML 拼
4. **合成**：所有页装进一个 `index.html`，← → / 空格 / 点击翻页，`fit.js` 全屏自适应
5. **预览**：`scripts/preview.sh` 用 playwright 缓存里的 chrome-headless-shell 截图

## 仓库结构

```
visual-deck/
├─ SKILL.md                      # 技能定义（Claude 读这个执行）
├─ assets/
│  ├─ skeleton/
│  │  ├─ visual-page.html        # 视觉页模板（底图 + flex 居中叠字）
│  │  ├─ info-page.html          # 信息页模板（组件库拼装）
│  │  └─ deck.html               # 合成翻页骨架（翻页 JS + 入场动效）
│  ├─ style-claymation.css       # 现成组件库（黏土风为默认，改 :root 变量即换风格）
│  └─ fit.js                     # 全屏等比缩放
├─ references/
│  ├─ imgen-prompts.md           # imgen 出底图 / 素材的 prompt 模板
│  └─ pitfalls.md                # 踩坑清单（动手前必读）
└─ scripts/
   ├─ preview.sh                 # headless 截图预览
   └─ chroma_cut.py              # 白底素材抠透明（连通域色键）
```

## 依赖

信息页那一半是**纯 HTML/CSS**，不需要任何 AI 工具——只有「视觉页底图」和「抠透明素材」用到外部工具。

| 用途 | 依赖 | 安装 / 说明 |
|---|---|---|
| 截图预览 | playwright 的 chromium | `npx playwright install chromium`（`preview.sh` 自动找缓存路径，本机没装 Chrome 也能用） |
| 出视觉页底图 / 素材 | 一个文生图 CLI | 见下方「关于 imgen」；信息页不需要它 |
| 抠透明素材（可选） | Python 3 + Pillow + numpy + scipy | `pip install pillow numpy scipy`；`chroma_cut.py` 连通域色键，保护主体内部浅色孔洞 |

### 关于 `imgen`

skill 里出底图调的是 `imgen`——作者环境里一个**基于 Codex 的文生图 / 图生图 CLI**（`imgen "<prompt>" -s 1536x864 -q high -o bg.png`），**不是 `npm install` 就有的通用公开工具**。换到你的环境，两条路任选其一：

- 把你自己的「文生图 CLI（输出 PNG）」装成 / 别名成 `imgen`，参数对齐 `-s`(尺寸) `-q`(质量) `-o`(输出)，调用样例见 [`references/imgen-prompts.md`](references/imgen-prompts.md)；
- 或用任意工具先按 prompt 模板的构图（主体一侧、另一侧留白、**图里不放文字**）把底图生成好，直接丢进页面当 `background`。

只用信息页 / 组件库 / 翻页骨架的话，连文生图都不用，纯 HTML 即可。

## 安装（作为 Claude Code 技能）

clone 到项目级或全局的 skills 目录：

```bash
# 全局（所有项目可用）
git clone https://github.com/xiaomoBoy/visual-deck.git ~/.claude/skills/visual-deck

# 或项目级
git clone https://github.com/xiaomoBoy/visual-deck.git <你的项目>/.claude/skills/visual-deck
```

装预览依赖（按需）：

```bash
npx playwright install chromium      # 截图预览（建议装）
pip install pillow numpy scipy       # 仅在要抠透明素材时
```

之后在 Claude Code（或其他读取 `SKILL.md` 执行的 AI agent）里说「**做个演示稿 / 把这个选题做成图 / 给大纲配图 / 做知识卡 / 把流程画出来**」即可触发，agent 会读 `SKILL.md` 按流程执行。`SKILL.md` 只用 shell 命令（`imgen` / `preview.sh` / `chroma_cut.py`），不绑定任何特定 agent 的工具。

## Quick start（手动跑一遍，不经 Claude）

想先不依赖 Claude 直接看效果：

1. **信息页**：复制 `assets/skeleton/info-page.html` + `assets/style-claymation.css` + `assets/fit.js` 到一个目录，照组件库的 class（卡片 / 波形 / 时间线 / 字幕表 / 终端 / 标签云 / 步骤条）把内容拼进 `.sbody`；
2. **视觉页**：复制 `assets/skeleton/visual-page.html`，把里面的 `BG.png` 换成你的留白底图；
3. **合成翻页**：把每页塞进 `assets/skeleton/deck.html` 的 `.slide` 里，浏览器打开，`← →` / 空格 / 点击翻页，`fit.js` 自动全屏缩放；
4. **截图预览**：`bash scripts/preview.sh deck.html out.png`（默认 1920×1080）。

换风格：改 `style-claymation.css` 里 `:root` 的 CSS 变量（配色 / 字体 / 圆角）+ 标题样式即可，黏土只是默认示例。

## 踩坑速查

完整清单见 [`references/pitfalls.md`](references/pitfalls.md)。最高频的几个：

- imgen **不支持透明背景** → 出白底再用 `chroma_cut.py` 抠
- 竖图素材塞进扁横条**脸只剩一半** → 用横向构图 prompt 出「视频帧」素材
- 全屏 **letterbox 边条色差** → `body` 底色 = slide 边缘色；整图封面四边不均匀要 radial mask + inset rim 让四边融进底色
- 封面标题**跑右上 / 往下掉** → 用 flex 居中，别用 transform 居中（会被入场动效的 `translateY(0)` 盖掉）；重新 flex 化 `.slide` 要写 `flex-direction:row`
- 单页内容**溢出 1080** → 压元素高度 / 间距

## 来源说明

本 skill 从一个个人短视频项目里抽出来，已脱去项目专属设定（沙盒规则 / 目录约定 / 特定受众 / 对其他私有 skill 的引用），方法论与踩坑清单是通用的。底图视觉默认是黏土风，改 `style-claymation.css` 的 `:root` 变量（配色 / 字体 / 圆角）+ 标题样式即可换成任意风格（玻璃科技 / 等距 2.5D / 杂志极简…）。

## Platform

Tested on macOS. Other platforms may work but are not verified — `preview.sh` 用了 bash + macOS playwright 缓存路径，Linux/Windows 需按本机环境调整。

## License

MIT — see [LICENSE](LICENSE).

# 踩坑清单（动手前读一遍，省下重蹈覆辙的时间）

这些都是真实踩过的坑，每条都让人卡过一阵。

## 1. imgen 不支持透明背景

`imgen ... -b transparent` 会报 **400「Transparent background is not supported」**。
→ 解法：出**白底图**，prompt 末尾加 `on a plain flat pale cream background, clear silhouette easy to cut out`，再用抠图工具去背景。

## 2. 抠透明两条路

- **`scripts/chroma_cut.py`（首选）**：连通域色键，只去掉「和图像边缘连通的背景」，**保护主体内部孔洞**——比如带浅色屏幕的笔记本、白色区域不会被误删。需要 scipy + PIL（anaconda 自带）。
  ```bash
  python3 scripts/chroma_cut.py in.png out.png [阈值默认52]
  ```
- **`npx hyperframes remove-background in.png -o out.png`**：u2net human_seg 模型，对人物/单一主体很好，CoreML 加速。首次下 168MB 模型。图标也能抠（碰巧 work），但对「主体内部有浅色孔」的图不如连通域色键。

## 3. 竖图素材塞进扁横条 → 脸只剩一半

时间线/列表里要放「视频帧缩略」时，**别用竖向半身人物图** cover 进扁横条——cover 只会显示一个横切片，脸永远不全，调 `background-position` 也救不了（横条根本放不下完整竖脸）。
→ 解法：专门用**横向构图** prompt 出一张「视频帧」素材（头肩对镜头、landscape 16:9），cover 进横条就能显示完整脸。见 `imgen-prompts.md` 的「横向视频帧」。

## 4. 全屏左右/上下色差

底图用「16:9 居中 + 缩放留白」时，全屏播放留白处的底色和图不一致 → 色差块。
→ 解法：底图 `background: url(...) center/cover` **铺满整个视口**（`position:fixed;inset:0`），任何屏幕比例都无留白、无色差。文字用 **vw 单位**叠在安全区（HTML 层不会被裁，只有底图边缘可能裁掉冗余）。

**叠字遮罩还藏一个色差**：给底图叠白色遮罩压出文字区时，别用**斜向**渐变（如 `linear-gradient(100deg,…)`）——倾斜角会让某一角白色覆盖不足，把 imgen 底图本就不均匀的光斑/色块漏在文字**正后方**。改成**水平 `90deg` + 文字安全区一段实心近白「平台」再淡出**：`linear-gradient(90deg,#f3f8ff 0 40%,rgba(243,248,255,.6) 56%,transparent 72%)`，文字区彻底铺平、零色差。验证时在**没有文字的空白边距**采样像素，别穿过文字胶囊/笔画（会把它们误判成色差）。

**最坑的一层（合成进 deck 后才暴露）**：单页 `position:fixed;inset:0` 的底图确实铺满视口，但**装进 deck 就不铺满了**——deck 被 `fit()` 等比缩放居中，窗口不是正好 16:9 时四周会露出 `body` 背景的 letterbox 边条。所以 **body 底色必须 = slide 边缘色**（deck.html 注释早有提醒），别给 body 用和封面不一致的渐变，否则 deck 边缘一条色差缝。
**整图封面更麻烦**：full-bleed imgen 封面四边本身就不均匀（如左白右蓝），单一 body 色没法同时贴合四边 → 哪条边反差大就在哪冒缝。解法：① body 设成封面**主边缘色**（如左字封面取左缘近白色）；② 给封面底图加 **radial mask** 让四边淡出 + 一层 **inset box-shadow 同色内描边**羽化外圈，让封面四边都融进 body 色，任何方向的边条都无缝（注意：mask 会连 box-shadow 一起裁，rim 要放在**没被 mask 的另一层**，如 `.cover-slide::before`）。验证：分别用比 16:9 **更宽**和**更高**的窗口截图，扫 deck 四缘像素，ΔR 都接近 0 才算过——只在 1920×1080 下采样会漏掉边条这层。

## 5. 单页内容溢出 1080

信息页元素塞太多会超出 1080 被截（底部内容/时间轴消失）。
→ 解法：压缩元素高度和间距（卡片 padding、行间 margin、标题 `margin-bottom`），别硬塞。`.sbody{justify-content:center}` 让内容垂直居中，但前提是内容总高 < 可用高。

## 6. 本机没装 Chrome 也能截图预览

系统 Chrome 可能不存在。playwright 装过的话，缓存里有 headless chromium：
- macOS arm64：`~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell`
- macOS x64 / Linux：同结构，架构目录是 `…-mac-x64` / `…-linux64`；Linux 缓存根是 `~/.cache/ms-playwright`
`scripts/preview.sh` 已封装好跨平台查找（两种缓存根 × 各架构通配 + 系统 chrome 兜底）。`--virtual-time-budget=1500` 让入场动效跑完再截、`--force-device-scale-factor=2` 出高清。

## 7. imgen 能出中文，但只信标题

imgen 出中文标题大字基本准，但**正文小字、密集文字偶有错字/乱码**。所以：抽卡定风格时「只看风格别看字」；关键准确文字一律交给 HTML 叠，别指望 imgen 把一屏文字都拼对。

## 8. 入场动效的 transform 覆盖了居中用的 transform

deck.html 给标题块上了 `animation:rise`，而 rise 的结束帧是 `transform:translateY(0)`。如果同一个标题块又用 `transform:translateY(-50%)` 做垂直居中，**动画结束帧会盖掉居中位移**（同元素两个 transform，动画赢）→ 标题从中线掉下去 / 跑偏。
→ 解法：**居中交给 flex（父级 `align-items:center`），不要用 transform 居中**；transform 只留给入场位移（translateY 40→0），两者不再打架。本 skill 的 `visual-page.html` 已改成 flex 居中。

## 9. 在 .slide 上重声明 flex，忘了 flex-direction

基类 `.slide` 是 `display:flex;flex-direction:column`。封面/特殊页想垂直居中又写了 `display:flex;align-items:center`，但**漏了 `flex-direction:row`** → 仍是 column：`align-items:center` 变成**水平**居中、`justify-content` 默认 `flex-start` 把内容顶到**最上**。症状：标题卡在「右上 / 上方」，调 margin 也救不回来。
→ 解法：重新 flex 化 `.slide` 时**显式写 `flex-direction:row`**。要「左字右图」就 `flex-direction:row;align-items:center;justify-content:flex-start` + 文字块 `margin-left`。

## 10. 波形/EQ 用满圆角 + 少量粗条 → 看着像一串泡泡

`.wave i{flex:1;border-radius:999px}` 只放 ~18 根，每根被撑到 ~70px 宽 + 全圆角，读成气泡不是波形。
→ 解法：放**多根细条（~28–40 根）**、小圆角（4–6px）、`align-self:center` 做上下对称，就是「语音备忘录」那种波形识别度。

## 11. 默认风格取向（可按项目改）

- 标题字偏**扁平描边**（白字+彩色描边+轻阴影），**不要厚重 3D 挤出字**（实测易被退回）
- 信息页别堆太满，留白舒服；默认面向非技术读者，文案直白
- 经历/数字/踩坑**不编**，没有就留 `> [!待补]` 问用户

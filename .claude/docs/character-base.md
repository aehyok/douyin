## 统一人物底座（视觉 IP）

`deck/character/` 是整个工作区的**统一人物底座**——所有产物（`deck/`、`ai-agent-video/` 等）的封面 / 视觉页 / 口播配图 / IP 形象都用这一个，保持形象一致、不要各做各的。

- 设定文档：`deck/character/persona.md`（外形 / 服装 / 粘土风规格 / imgen 主体描述槽位）
- 当前主形象：`persona-clay-v2.png`（东亚青年男 + 黑框矩形眼镜 + 珊瑚橘短袖 + 笔记本印 Apple 图标，3D 粘土定格风），配薰衣草紫背景
- 备份：`persona-clay.png`（早期藏青连帽版）
- **三个辨识锚点每次出图必保留**：黑色细框矩形眼镜 / 珊瑚橘短袖 / 笔记本上的发光白色 Apple 图标
- 出人物图优先 img2img 引用 `persona-clay-v2.png`；纯 prompt 用 `persona.md` 第六节的「主体片段」。出图**不要透明背景**（imgen 后端不支持）。

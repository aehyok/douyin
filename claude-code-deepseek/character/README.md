# AI 少年 · 黏土风人物素材

基于本人照片用 `imgen` img2img 生成的 3D 黏土风格角色形象，抠透明后可复用。

## 文件

| 文件 | 说明 | 尺寸 |
|---|---|---|
| `portrait.png` | 正面头像，微笑，透明背景 | 1024×1024 |
| `waving.png` | 半身挥手，透明背景 | 1024×1024 |

## 风格参数

- **风格**：3D clay claymation，soft matte plasticine
- **出图工具**：`imgen` (Codex CLI)，`-q high`，img2img 模式（以本人照片为参考）
- **抠透明**：`chroma_cut.py`（连通域色键，阈值 52）

## 用途

- 演示稿封面/结尾底图（已用于 `claude-code-deepseek/deck/`）
- 信息页小图标/头像
- 视频缩略图素材

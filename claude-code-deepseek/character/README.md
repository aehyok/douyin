# AI 少年 · 固定人物素材

> ⚠️ **以全局底座为准**：整个工作区的统一人物底座是仓库根的 [`character/persona-clay-v5.png`](../../character/persona-clay-v5.png)（设定见 [`character/persona.md`](../../character/persona.md)），「不要各做各的」。本目录是 `claude-code-deepseek` 项目早期自建的本地素材，**仅作历史快照保留**——新产出请优先用全局底座，三大辨识锚点一致即可（黑框矩形眼镜 / 珊瑚橘短袖 / 笔记本发光 Apple 图标）。

本目录保存 `claude-code-deepseek` 项目早期的人物参考与历史人物素材。

## 早期项目设定（历史，与全局底座一致即可）

本项目早期产物使用的人物设定（与全局底座同一形象，措辞略有差异）：

- 3D 黏土风格，soft matte plasticine texture。
- 年轻男性技术博主，正面坐在笔记本电脑前。
- 深棕/黑色蓬松分束头发。
- 黑色方框眼镜。
- 橙色短袖 T 恤。
- 温和微笑，亲和、干净、科技教程感。
- 浅紫色背景或同色系柔和背景。
- 笔记本电脑在前景。

固定参考图文件名：

| 文件 | 说明 |
|---|---|
| `reference-fixed.png` | 当前唯一指定的人物参考图：橙色 T 恤、黑框眼镜、坐在笔记本电脑前 |

注意：如果 `reference-fixed.png` 暂时不存在，说明参考图还只是聊天附件，尚未落盘。生成前应先把固定参考图放到这个文件名下。

## 历史文件

| 文件 | 说明 | 尺寸 |
|---|---|---|
| `portrait.png` | 早期紫色 hoodie 头像，历史素材，不再作为固定设定 | 1024×1024 |
| `waving.png` | 早期紫色 hoodie 半身挥手，历史素材，不再作为固定设定 | 1024×1024 |

## 生成约束

- 新图优先以全局底座 `../../character/persona-clay-v5.png` 为 img2img / reference image（本地 `reference-fixed.png` 仅作历史参考）。
- 不要再生成紫色/蓝色 hoodie 版本。
- 不要改成其他发型、无眼镜、不同年龄感的人物。
- 不要把人物改成扁平卡通、写实照片、赛博朋克、二次元等风格。
- imgen 底图不要放中文正文，准确文字交给 HTML。

参考提示词：

```text
3D clay claymation style, same character as the reference image: a young Chinese male tech creator with dark tousled hair, black square glasses, orange T-shirt, sitting behind a laptop, gentle smile, soft matte plasticine texture, clean tutorial creator look, pale lavender background, horizontal 16:9 composition, leave clean empty space for HTML title overlay, NO text anywhere in the image.
```

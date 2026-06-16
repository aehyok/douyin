# claude-code-deepseek 项目约定

本目录是「从零安装 Claude Code 并接入 DeepSeek」这期内容的独立项目。后续生成演示稿、封面、结尾页、人物素材、视频帧或任何视觉图时，必须优先遵守本文件。

> ⚠️ **以全局底座为准**：人物形象统一用仓库根的 `../character/persona-clay-v5.png`（设定见 `../character/persona.md`），「不要各做各的」。本目录下的 `character/reference-fixed.png` 是早期本地素材，仅作历史快照——新产出请用全局底座，下面的特征描述与之一致，措辞略有差异。

## 固定人物设定

人物形象统一用全局底座，不要随意重画成其他形象。

参考图（优先全局底座）：

- `../character/persona-clay-v5.png`（全局底座，首选）
- `character/reference-fixed.png`（本项目早期本地素材，历史参考）

固定角色特征：

- 3D 黏土风格，soft matte plasticine texture。
- 年轻男性技术博主，正面坐在笔记本电脑前。
- 深棕/黑色蓬松分束头发。
- 黑色方框眼镜。
- 橙色短袖 T 恤。
- 温和微笑，亲和、干净、科技教程感。
- 浅紫色背景或同色系柔和背景。
- 笔记本电脑在画面前景，作为教程/开发者身份识别。

禁止事项：

- 不要改成紫色/蓝色 hoodie。
- 不要改成其他发型、无眼镜、不同年龄感的人物。
- 不要把人物改成卡通扁平、写实照片、赛博朋克、二次元等风格。
- 不要在 imgen 底图里生成中文正文；准确文字交给 HTML。

## 生成视觉页时的提示词基准

需要生成新底图时，以全局底座 `../character/persona-clay-v5.png` 作为 img2img / reference image（本地 `character/reference-fixed.png` 仅作历史参考）。提示词可从下面这段改：

```text
3D clay claymation style, same character as the reference image: a young Chinese male tech creator with dark tousled hair, black square glasses, orange T-shirt, sitting behind a laptop, gentle smile, soft matte plasticine texture, clean tutorial creator look, pale lavender background, horizontal 16:9 composition, leave clean empty space for HTML title overlay, NO text anywhere in the image.
```

如果工具不支持参考图，也必须按上面的固定角色特征手写 prompt，保持人物一致。

## 历史素材说明

`character/portrait.png` 和 `character/waving.png` 是早期紫色 hoodie 版本，仅作为历史素材保留。新产出不得再以它们作为主要人物设定。

## 输出规则

- 新版本演示稿放到新目录，例如 `deck_v4/`，不要覆盖已有 `deck/`、`deck_v2/`、`deck_v3/`。
- 字幕内容以 `字幕.md` 为准；字幕没有给出的经历、数字、命令细节不要自行补全。
- 视觉页用底图 + HTML 叠字；信息页优先用 HTML/CSS，保证中文准确。

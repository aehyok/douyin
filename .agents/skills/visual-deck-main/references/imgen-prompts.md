# imgen prompt 模板

imgen 的 prompt **英文质量更好**；要图里出中文时，把中文文字用引号明确写进 prompt（但记住坑 #7：只信标题大字）。

## A. 视觉页「留白底图」（路线 B 的核心）

目标：主体在一侧、另一侧大面积留白、**图里不放主标题文字**，给 HTML 叠字腾地方。出不透明整图，当背景用。

模板：
```
3D <风格> style horizontal 16:9 banner background. <主体描述>, placed on the RIGHT third of the frame. The LEFT two-thirds is clean empty <留白色> space reserved for a title to be added later. <可选装饰: clouds, stars...>. <质感词>. NO text anywhere in the image.
```

实例（黏土风封面底图）：
```
3D clay claymation style horizontal 16:9 banner background. A cute boy with black curly hair in a purple hoodie sitting at a desk with a laptop, clapperboard and plant, placed on the RIGHT third. The LEFT two-thirds is clean empty soft lavender-purple space reserved for a title. Cute clouds and a star top-right. Soft matte plasticine texture. NO text anywhere in the image.
```
尺寸 `-s 1536x864`（16:9）。留白侧可左可右，和 HTML 叠字位置对应即可。

## B. 横向「视频帧」素材（给信息页里的片段缩略）

避开坑 #3：要横向头肩构图，cover 进横条才显示完整脸。
```
3D <风格> style, <人物> talking to camera, head and shoulders portrait, soft plain studio background, horizontal landscape framing, face fully visible and centered, <质感词>
```
尺寸 `-s 1536x864`。这种当 clip 背景用 `background:linear-gradient(色罩),url(...);background-size:cover`，色罩区分不同状态（如删除前紫罩/删除后绿罩）。

## C. 白底素材（图标/小人/物件，待抠透明）

避开坑 #1：出白底，末尾必加便于抠图的话。
```
3D <风格> app icon of <物件>, <颜色> rounded, soft matte texture, glossy highlight, centered, on a plain flat pale cream background, clear silhouette easy to cut out
```
出图后用 `scripts/chroma_cut.py` 抠透明。

## D. 风格词参考（换风格改这里，黏土只是默认）

| 风格 | 关键词 |
|---|---|
| 黏土 3D（默认） | `3D clay claymation, soft matte plasticine, rounded` |
| 亮色卡通 | `bright flat-cartoon, bold black outline, vivid, playful` |
| 等距 2.5D | `isometric 2.5D, soft pastel tech palette, dimensional` |
| 玻璃科技 | `clean light-tech, glassmorphism, frosted, soft blue-white` |
| 杂志极简 | `editorial minimalist, white space, thin lines, serif accent` |

## 抽卡定风格的方法

做之前先抽卡：同一构图用 4-6 个不同风格词各出一张，**只看风格调性别看字**，让用户挑一个定下来。挑定后整套统一用这个风格。

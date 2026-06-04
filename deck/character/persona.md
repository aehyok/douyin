# 人物设定 · AI 内容创作者 / 视频博主（粘土风格）

> 来源：基于参考头像 `e18dbeefa9b7cccc418d20e8081fe22f.jpg` 提炼，转译为 3D 粘土定格动画（claymation）气质。
> 用途：visual-deck 视觉页的「主体」、封面人物、口播配图、IP 形象统一参考。

## 一、核心气质（一句话）

一位安静、书卷气、技术宅感的东亚青年男生，戴黑框眼镜，是个专注做内容的 AI 视频博主——温和、可亲、不张扬。

## 二、外形属性

| 属性 | 设定 | 英文（imgen 用） |
|---|---|---|
| 性别 / 族裔 | 东亚青年男性 | young East Asian man |
| 年龄感 | 约 22–26 岁 | early-to-mid 20s |
| 发型 | 蓬松微乱的中长发，自然中分偏右，刘海略垂额前与脸侧 | tousled medium-length dark brown hair, soft messy fringe |
| 发色 | 深棕（近黑） | dark brown, almost black |
| 眼镜 | **黑色细框矩形眼镜**（标志性，必保留） | thin black rectangular glasses |
| 脸型 | 清秀偏瘦，下巴略尖 | slim gentle face |
| 表情 | 平静温和，淡淡微笑（封面可更亲和） | calm friendly, soft smile |
| 肤色 | 自然暖白 | warm fair skin |

## 三、服装

| 部位 | 设定 | 英文 |
|---|---|---|
| 上装 | **珊瑚橘 / 三文鱼色短袖 T 恤**（当前主形象） | coral / salmon short-sleeve t-shirt |
| 整体 | 简洁清爽的单件短袖，创作者日常感 | clean casual creator look, single short-sleeve tee |
| 道具 | 身前一台笔记本，**机盖朝镜头、印一个发光白色 Apple 图标**（直播感） | a laptop with the lid facing camera, small glowing white Apple logo on the back |

## 四、粘土风格规格（视觉统一锚点）

- 风格词：`3D clay claymation style, soft matte plasticine texture, rounded forms, handmade stop-motion look`
- 质感：哑光橡皮泥、圆润体块、轻微指纹手作感、柔和棚光
- 比例：略卡通化的大头友好比例（比写实更圆、更可爱）
- 配色锚点：人物 **珊瑚橘短袖**，搭配 **柔和薰衣草紫** 背景（与 visual-deck 默认色板 `#7a5ce0 / #6a4fd0`、高亮 `#f6c945` 一致）——暖橘在紫底上正好跳出来

## 五、博主道具（按页面需要取用）

笔记本电脑、麦克风、场记板（clapperboard）、相机、绿植、漂浮的 AI 元素（小机器人 / 对话气泡 / 神经网络节点）。

## 六、可直接复用的 imgen「主体描述」槽位

> 填进 `imgen-prompts.md` 模板 A 的 `<主体描述>` 处。

**主体片段（人物本体）：**
```
A cute young East Asian man with tousled dark brown hair and thin black rectangular glasses, calm friendly soft smile, wearing a coral/salmon short-sleeve t-shirt, with a laptop in front of him, the lid facing the camera showing a small glowing white Apple logo
```

**封面整句（留白底图，左侧留白给标题）：**
```
3D clay claymation style horizontal 16:9 banner background. A cute young East Asian man with tousled dark brown hair and thin black rectangular glasses, calm friendly soft smile, wearing a coral/salmon short-sleeve t-shirt, sitting at a desk behind an open laptop with the lid facing the camera showing a small glowing white Apple logo, microphone and a small plant, glowing floating AI chat bubbles around him, placed on the RIGHT third of the frame. The LEFT two-thirds is clean empty soft lavender-purple space reserved for a title to be added later. Cute clouds and a star top-right. Soft matte plasticine texture, rounded handmade forms. NO text anywhere in the image.
```

## 七、注意

- **眼镜是辨识锚点**，每次出图都要带上 `thin black rectangular glasses`。
- **珊瑚橘短袖 + 笔记本上的 Apple 图标** 是当前形象的另外两个锚点，出图尽量保留。
- 当前主形象文件：`persona-clay-v2.png`（珊瑚短袖版）；`persona-clay.png` 是早期藏青连帽版，留作备份。
- 出图**不要透明背景**（imgen 后端不支持，报 400）；要抠图先出白底再用 chroma_cut。
- 标题文字不进底图（`NO text anywhere`），交给 HTML 叠字。

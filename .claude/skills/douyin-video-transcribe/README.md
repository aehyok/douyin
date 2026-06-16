# douyin-video-transcribe — 抖音链接 → mp4 + 文字

本工作区的自研 skill：解析抖音分享链接 → 下载无水印视频 → 用 FunASR 把音频转成文字。是「视频流水线」的入口环节（转写毛坯 → `transcript.md` → `script.md` → deck → 成片）。

## 现状（开箱即用）

- ✅ venv 已建好：`scripts/venv/`，torch / torchaudio / funasr 全部装好，**不要用系统 Python，也不要重新 setup**
- ✅ 输出位置自动化：在 skill 目录执行时，产物自动落到**项目根**的 `作者-标题前20字/` 子目录（`<视频ID>.mp4` + `.txt`）
- ⚠️ 唯一外部依赖：系统需有 FFmpeg（本机已装，新机器自行 `brew install ffmpeg` 或加 PATH）

## 用法

### macOS

```bash
.claude/skills/douyin-video-transcribe/scripts/venv/bin/python \
  .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<分享链接>" --transcribe
```

### Windows（必须先清代理 + 强制 UTF-8）

```bash
unset ALL_PROXY all_proxy HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 .claude/skills/douyin-video-transcribe/scripts/venv/Scripts/python.exe \
  .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<分享链接>" --transcribe
```

不清代理会被 SOCKS 挡请求；不强制 UTF-8 会在标题含 emoji 时撞 GBK 崩溃。这两个坑是 Windows 特有的。

### 参数

| 参数 | 说明 |
|---|---|
| `<分享链接>` | 必填。支持 `v.douyin.com`、`www.iesdouyin.com/share/video/`、`www.douyin.com/video/` 三种格式 |
| `--transcribe` | 下载后转文字（FunASR，默认模型 `paraformer-zh` + `fsmn-vad` + `ct-punc`） |
| `--model` / `--vad-model` / `--punc-model` | 自定义 ASR / VAD / 标点模型，一般不用动 |
| `--output-dir` | **🚫 绝不要传**，见下 |

### ⚠️ 为什么不能传 `--output-dir`

脚本检测到在 skill 目录（存在 `SKILL.md`）执行时，会自动按 `作者-标题前20字`（`sanitize_title_for_dir` 清洗+截断）在**项目根**建独立选题目录存放产物——这正是仓库「一个选题一个目录」的命名惯例。一旦手动传 `--output-dir`，这套逻辑被覆盖，文件会落到 skill 内的 `downloads/`，还得手动归位。

## 输出

```
<仓库根>/<作者-标题前20字>/
├── <视频ID>.mp4   # 无水印视频
└── <视频ID>.txt   # 转写文字（--transcribe 时生成）
```

后续流程：把 `.txt` 整理成 `transcript.md`（毛坯），再润色成 AI少年口播版 `script.md`，详见 `.claude/docs/video-pipeline.md`。

## 目录结构

```
douyin-video-transcribe/
├── README.md                      # 本文件（面向人）
├── SKILL.md                       # skill 文档（面向 agent）
└── scripts/
    ├── parse_douyin_video.py      # 主脚本：解析 + 下载 + 调转写
    ├── transcribe_audio_funasr.py # FunASR 转写
    ├── setup_venv.py              # 建 venv（仅新机器初始化用）
    ├── run.py / run.sh / run.bat  # 上游遗留的启动脚本，本仓库不用
    └── venv/                      # 已就绪的虚拟环境（不入 git）
```

## 新机器初始化

仅当换机器、venv 不存在时才需要：

```bash
cd .claude/skills/douyin-video-transcribe
python scripts/setup_venv.py   # 提示安装 FunASR 时输入 y
```

torch + funasr 体积大（数 GB），首次转写还会下载模型，需稳定网络与磁盘空间。

## 故障排查

| 现象 | 原因 / 解法 |
|---|---|
| `ffmpeg: command not found` | 装 FFmpeg：macOS `brew install ffmpeg`；Windows 下载后把 `bin` 加 PATH |
| 请求失败 / 连接被拒（Windows） | 没清代理，先 `unset ALL_PROXY ...`（Clash TUN 会劫持流量） |
| `UnicodeEncodeError`（GBK） | 没加 `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` |
| `No module named funasr` | 用了系统 Python，改用 `scripts/venv/` 内的解释器 |
| 文件落到了 skill 的 `downloads/` | 传了 `--output-dir`，去掉重跑 |
| 解析失败 | 链接被删 / 设为私密，或链接格式不对 |
| 图集链接 | 脚本会识别并提示，不会按视频下载 |

## 免责声明

仅供学习研究。

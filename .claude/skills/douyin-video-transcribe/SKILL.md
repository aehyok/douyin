---
name: douyin-video-transcribe
description: 解析抖音分享链接，下载视频，并使用FunASR将视频音频转成文字。当用户提供抖音分享链接（v.douyin.com、www.iesdouyin.com、www.douyin.com）时，自动解析链接获取视频信息，下载视频文件，并可选择性地将视频中的音频转换为文字。支持视频和图集两种内容类型。
---

# 抖音视频转文字

解析抖音分享链接 →（无水印）下载视频 →（可选）用 FunASR 把音频转文字。支持视频和图集两种内容。

## ⚡ 本仓库快速开始（venv 已装好，直接用）

> 本工作区的 `scripts/venv/` 已经装好 torch / torchaudio / funasr，**直接用它**，别走系统 Python、别跑 `run.py`/`setup_venv.py`（那是给空环境第一次装用的，见文末附录）。

**铁律（先记住，再跑）：**
- **绝不要传 `--output-dir`。** 不传时脚本会自动在**项目根**按 `作者-标题前20字` 建子文件夹，存 `<视频ID>.mp4` + `.txt`；一旦手动传，文件会落到 skill 内的 `downloads/`，破坏归档。
- venv 解释器路径**按平台区分**：macOS 是 `scripts/venv/bin/python`，Windows 是 `scripts/venv/Scripts/python.exe`。

**macOS / Linux：**
```bash
.claude/skills/douyin-video-transcribe/scripts/venv/bin/python \
  .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<链接>" --transcribe
```

**Windows（必须先清代理 + 强制 UTF-8，否则撞 GBK emoji 崩溃 / SOCKS 挡 pip）：**
```bash
unset ALL_PROXY all_proxy HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 .claude/skills/douyin-video-transcribe/scripts/venv/Scripts/python.exe \
  .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<链接>" --transcribe
```
> 这两个坑是 Windows 特有的，macOS 上无需处理。

只下载、不转文字：去掉 `--transcribe` 即可。

## 工作流程

1. **解析分享链接** — 兼容 App 分享链接和 PC 端链接
2. **提取视频信息** — 标题、作者、封面等
3. **下载视频** — 自动把 `playwm` 换 `play` 拿无水印 MP4，处理 302 重定向到真实 CDN
4. **音频转文字**（可选，`--transcribe`）— FunASR 识别，首次会下载模型（约几 GB）

## 完整参数

```bash
python scripts/parse_douyin_video.py <分享链接> \
  --transcribe \            # 是否转文字
  --model paraformer-zh \   # ASR 模型，默认 paraformer-zh
  --vad-model fsmn-vad \    # VAD 模型，默认 fsmn-vad
  --punc-model ct-punc      # 标点恢复模型，默认 ct-punc
```

## 输出

- 视频：`<视频ID>.mp4`；转写：`<视频ID>.txt`
- 不传 `--output-dir`（推荐）时，二者落到**项目根**按 `作者-标题前20字` 建的子文件夹（标题不可用时回退到视频 ID）
- 终端还会打印视频信息和 JSON 格式的完整结果

## 脚本说明

- **`parse_douyin_video.py`** — 主脚本：解析链接 / 取视频信息 / 下载 / 调用转写。函数 `parse_share_url()`、`parse_video_id()`、`download_video()`；带 `--transcribe` 时自动调同目录 `transcribe_audio_funasr.py`。
- **`transcribe_audio_funasr.py`** — 语音识别，提供 `transcribe_audio()`；支持 FunASR Python API（首选）与命令行（`--audio <音频>`），含时间戳提取。
- **`run.py` / `run.sh` / `run.bat`、`setup_venv.py`** — 仅用于**首次/重装环境**（自动建 venv + 装依赖），本仓库 venv 已就绪，平时不用，详见附录。

## 故障排查

1. **Windows：GBK 报错 / pip 被 SOCKS 代理挡**（最常见）
   - 现象：emoji 触发 `UnicodeEncodeError: 'gbk'`；或装依赖时 `Missing dependencies for SOCKS support`
   - 解决：按上面「Windows 快速开始」先 `unset` 代理 + `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` 再跑
2. **`ffmpeg: command not found`** — FFmpeg 是系统级工具，需单独装（macOS `brew install ffmpeg`；Ubuntu `sudo apt install ffmpeg`；Windows 下载解压后把 `bin` 加进 PATH），`ffmpeg -version` 验证
3. **`No module named 'requests'/'funasr'`** — 说明没用自带 venv。确认用的是 `scripts/venv/.../python`，而不是系统 Python
4. **转文字失败** — 确认 venv 里依赖在位：`pip list | grep -E "(torch|torchaudio|funasr)"`；首次需下模型，确保网络稳定；torch 慢可加 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
5. **无法解析链接 / 下载失败** — 检查链接是否有效（未删除、非私密）、网络连通、磁盘空间与写入权限
6. **图集链接** — 脚本会识别并提示，不会当视频下载

---

## 附录：首次 / 重装环境（本仓库通常用不到）

仅当 `scripts/venv/` 不存在或损坏时才需要。

**前提**：Python 3.8+、FFmpeg（系统级，见故障排查 2）。

**自动建环境（推荐给空环境）：**
```bash
cd .claude/skills/douyin-video-transcribe
python scripts/run.py "<链接>"            # 检测并自动建 venv + 装基础依赖后运行
# 或手动：
python scripts/setup_venv.py             # 建 venv，提示是否安装 FunASR（转文字需要）
```

**手动装依赖**（venv 激活后）：
```bash
pip install requests urllib3                       # 基础（解析/下载）
pip install torch>=1.13 torchaudio funasr>=1.0.0   # 转文字（必须按此顺序：先 torch/torchaudio 再 funasr）
```
> FunASR 要求 Python ≥ 3.8、torch ≥ 1.13；torch/模型体积大，预留 ≥ 5GB 磁盘。

## 抖音转写（链接 → mp4 + 文字）

收到抖音分享链接时用 `douyin-video-transcribe` skill 解析 + 下载 + 转写（FunASR）。**此工作区在 macOS 和 Windows 两台机器上都会用**，跑之前先认清当前平台，硬约束如下：

- **绝不要传 `--output-dir`**（两平台通用）。脚本在 skill 目录（检测到 `SKILL.md`）执行时会自动在**项目根**按 `作者-标题前20字`（清洗+截断，见 `sanitize_title_for_dir`）建独立子文件夹存 `<视频ID>.mp4` + `.txt`；一旦传 `--output-dir` 就覆盖这套逻辑，文件会落到 skill 内的 `downloads/` 而非项目根。
- **直接用 skill 自带 venv**（`scripts/venv/`，已装好 torch/torchaudio/funasr），别走系统 Python。venv 解释器路径按平台区分：
  - macOS：`scripts/venv/bin/python`
  - Windows：`scripts/venv/Scripts/python.exe`
- **macOS** 直接跑即可：
  ```bash
  .claude/skills/douyin-video-transcribe/scripts/venv/bin/python \
    .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<链接>" --transcribe
  ```
- **Windows** 要先清代理 + 强制 UTF-8，否则会撞 GBK emoji 崩溃 / SOCKS 挡 pip 两个坑：
  ```bash
  unset ALL_PROXY all_proxy HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 .claude/skills/douyin-video-transcribe/scripts/venv/Scripts/python.exe \
    .claude/skills/douyin-video-transcribe/scripts/parse_douyin_video.py "<链接>" --transcribe
  ```
  （这两个坑是 Windows 特有的；macOS 上无需处理。）

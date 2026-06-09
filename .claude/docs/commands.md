## 常用命令

真正有构建/测试工具链的只有 `ai-agent-video/presentation/`（先 `cd` 进去）：

```bash
npm run dev                  # Vite 开发服务器
npm run build                # tsc -b 类型检查 + vite build
npm run lint                 # eslint .
npm run preview              # 预览 dist

npm run extract-narrations   # 扫所有 narrations.ts → audio-segments.json
npm run extract-narrations -- --print
npm run synthesize-audio     # 按 audio-segments.json 逐段合成 public/audio/<id>/<N>.mp3
npm run synthesize-audio -- --force                  # 强制重新合成
PRESENTATION_TTS=openai npm run synthesize-audio      # 切 TTS provider（默认 minimax）
npm run synthesize-audio -- --provider=elevenlabs --voice=Rachel
```

`deck/` 是纯静态，直接用浏览器打开 `deck/index.html` 即可（← → / 空格 / 点击翻页）。截图预览走 `visual-deck-main` skill 的 `preview.sh`（Windows 上的坑见全局 memory `preview-sh-windows-fix.md`）。

测试：本仓库目前**没有测试套件**。`verify-step-*.png` 是用 puppeteer-core 截图做的人工校验产物，不是自动化测试。

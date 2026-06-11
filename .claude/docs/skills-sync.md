## Skills 同步（重要）

`npx skills` 会把 skill 装到 `.agents/skills/`，但 Claude Code 实际读 `.claude/skills/`。**此工作区在 macOS 和 Windows 两台机器上都会用**，同步方式按平台区分：

- **macOS**：`npx skills add` 会自动建好 `.claude/skills/<name>` → `../../.agents/skills/<name>` 的 symlink，Claude Code 直接读到，**无需手动 copy**（装 hyperframes 时即如此）。
- **Windows**：symlink 不可靠，**add / update / remove skill 后要手动把 `.agents/skills/` 同步（copy）到 `.claude/skills/`**（项目级）。详见 `~/.claude/skills-sync.md`。

> 自研 skill（如 `douyin-video-transcribe`、`douyin-rule-check`）直接放 `.claude/skills/` 真实目录，不走 `.agents/`，无需同步。

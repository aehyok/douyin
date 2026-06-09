## Skills 同步（重要）

本机用户全局规则：`npx skills` 会把 skill 装到 `.agents/skills/`，但 Claude Code 实际读 `.claude/skills/`。Windows symlink 不可靠，所以 **add / update / remove skill 后要手动把 `.agents/skills/` 同步到 `.claude/skills/`**（项目级）。详见 `~/.claude/skills-sync.md`。

> macOS 上 `npx skills add` 会自动建好 `.claude/skills/<name>` → `../../.agents/skills/<name>` 的 symlink、Claude Code 直接读到，**无需手动 copy**（手动同步主要是 Windows 的坑）。装 hyperframes 时即如此。

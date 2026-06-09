# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 本文件已按主题拆分到 `.claude/docs/`，下面大部分用 `@import` 预加载。改某一节内容请直接编辑对应文件，不要在本文件里堆正文。

## 目录

- 这个仓库是什么 → `@.claude/docs/repo-overview.md`（预加载）
- 统一人物底座（视觉 IP） → `@.claude/docs/character-base.md`（预加载）
- 常用命令 → `@.claude/docs/commands.md`（预加载）
- presentation 应用架构（关键） → `.claude/docs/presentation-architecture.md`（**按需**，见下）
- Skills 同步（重要） → `@.claude/docs/skills-sync.md`（预加载）
- 抖音转写（链接 → mp4 + 文字） → `@.claude/docs/douyin-transcribe.md`（预加载）
- 视频流水线（文章 → mp4） → `@.claude/docs/video-pipeline.md`（预加载）
- 语言 → `@.claude/docs/language.md`（预加载）

## 按需加载（不预加载，相关时才读）

- **改 `ai-agent-video/presentation/`（那个伪装成视频的点击驱动网页）前，先用 Read 读 `.claude/docs/presentation-architecture.md`**，了解「单一真相源」约束（narrations.ts / 章节代码 / chapters.ts / 音频文件 5 处必须对齐）再动手，否则容易把 step 数改漂。

@.claude/docs/repo-overview.md
@.claude/docs/character-base.md
@.claude/docs/commands.md
@.claude/docs/skills-sync.md
@.claude/docs/douyin-transcribe.md
@.claude/docs/video-pipeline.md
@.claude/docs/language.md

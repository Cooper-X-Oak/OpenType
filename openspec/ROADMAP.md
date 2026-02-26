# OpenType Roadmap 🗺️

本文档记录了 OpenType 的未来开发计划和演进方向。旨在为后续开发（包括人类开发者和 AI 模型）提供清晰的指引。

## Phase 1: 交互体验升级 (UX Polish) 🌟
**核心目标**: 降低使用摩擦，提供清晰的反馈循环，打造“无感但有知”的体验。

- [x] **光标跟随指示器 (Cursor Indicator)**
  - 在当前光标位置显示极简状态（录音中🔴 / 处理中🔵）。
  - 解决用户视线离开焦点去查看托盘图标的问题。
  - 技术点: 获取光标坐标 (Windows API)，绘制无边框置顶窗口。
  - **更新**: 优化为极客风格的“终端方块光标” (Terminal Block Cursor)。

- [x] **音效反馈 (Sound Feedback)**
  - 极短的“滴”声提示开始录音和结束录音。
  - 实现真正的“盲操作”（Eyes-free usage）。
  - 允许在设置中开关。

- [ ] **流式输出 (Streaming Output)**
  - **状态**: 暂缓 (Deferred)
  - 经过评估，当前非流式方案兼容性更好，且流式直接上屏会干扰编辑器。
  - 未来可能考虑“悬浮窗预览”方案。

## Phase 1.5: 产品化与极客体验 (Productization & Geek Experience) 🛠️
**核心目标**: 完善软件生命周期管理，提供极客风格的配置与交互体验。

- [ ] **安装与卸载 (Installer & Uninstaller)**
  - 使用 Inno Setup 制作标准 Windows 安装包。
  - 支持一键安装、创建快捷方式、注册表清理。
  - **风格**: 保持安装过程简洁快。

- [ ] **极客风格引导与配置 (Geek Style Onboarding & Config)**
  - **交互界面**: 摒弃传统 GUI 设置窗口，采用类似 TUI (Text User Interface) 或 "Command Palette" 的设计。
  - **功能**:
    - 首次启动引导 (Setup Wizard)。
    - 多 API 管理 (DashScope, OpenAI, Local Whisper)。
    - 个性化配置 (热键、音效开关、光标样式)。
  - **历史记录**: 本地存储并管理历史输入记录 (Local History Manager)，支持检索和回溯。

## 性能与效率优化 (Efficiency & Performance) ⚡
**核心目标**: 打造极致轻量、快速响应的工具。

- [ ] **安装包瘦身 (Package Slimming)**
  - **现状**: 目前 60MB+ (包含全量 PySide6/DashScope)。
  - **目标**: 压缩至 30MB 以内。
  - **手段**:
    - 排除 PySide6 不用的模块 (QtWebEngine, Qt3D, QtQml)。
    - 使用 UPX 压缩 DLL。
    - 清理虚拟环境冗余依赖。

## Phase 2: 功能增强 (Power Features) 🚀
**核心目标**: 从简单的听写工具进化为生产力神器。

- [ ] **智能格式化 (Smart Formatting)**
  - 自动处理标点符号（目前 DashScope 已部分支持，需优化）。
  - 支持 Markdown 语法转换（如语音说“列表项”，自动转为 `- `）。

- [ ] **语音指令 (Voice Commands)**
  - 识别特定关键词执行操作。
  - 示例指令：
    - "换行" -> `Enter`
    - "删除上一句" -> `Ctrl+Z` 或 `Backspace`
    - "翻译成英文" -> 调用翻译 API 后输出

- [ ] **剪贴板优化 (Clipboard Optimization)**
  - 目前使用 `pyperclip` 会覆盖用户剪贴板内容。
  - 优化流程: `保存当前剪贴板` -> `写入文本` -> `粘贴` -> `恢复原剪贴板`。
  - 实现完全无副作用的文本注入。

- [ ] **多模型/多语言支持**
  - 支持中英混合输入（DashScope 增强版）。
  - 探索本地离线模型（如 Whisper tiny/base），为无网环境提供降级支持。

## Phase 3: 工程化与分发 (Engineering) 🛠️
**核心目标**: 提升软件的健壮性和易用性。

- [ ] **自动更新 (Auto-Updater)**
  - 启动时检查 GitHub Releases。
  - 提示新版本并支持一键下载更新。

- [ ] **崩溃报告与调试**
  - 增加“调试模式”选项，输出详细日志。
  - 简单的日志查看窗口。

- [ ] **安装包制作 (Installer)**
  - 使用 Inno Setup 或 NSIS 制作标准 Windows 安装包。
  - 支持“开机自启”选项配置。

---
*注：本文档由 OpenType 核心开发团队维护，后续 AI 模型在开发前请查阅此文档以对齐目标。*

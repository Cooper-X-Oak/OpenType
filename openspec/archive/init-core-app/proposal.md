## Why

当前市场上缺乏一个本地优先、极客友好且轻量级的语音输入增强工具。用户希望在 Windows 平台上实现类似 `opentypeless` 的“按住说话，松开上屏”的流畅体验，并希望该工具是一个完整的桌面应用，具备可视化配置和历史记录管理功能。

为了满足这一需求，我们将构建 **OpenType** —— 一个基于 Python + PySide6 的本地桌面应用，集成全局热键、WinMM 录音、Cloud STT（DashScope）和自动化文本注入功能。

## What Changes

我们将从零开始构建 OpenType 应用的核心功能：

*   **新增** 核心应用架构：基于 Python (Backend) + PySide6 (UI)。
*   **新增** 音频捕获模块：使用 WinMM API 实现低延迟录音。
*   **新增** 全局热键系统：使用 keyboard 库实现“按住说话”的交互模式。
*   **新增** STT 集成：接入 Cloud STT API (DashScope) 进行语音转文字。
*   **新增** 文本注入：模拟键盘输入将转录文本发送到当前活动窗口。
*   **新增** 系统托盘：支持最小化到托盘，后台运行。
*   **新增** 配置界面：提供 API Key 设置、热键自定义等选项。

## Capabilities

### New Capabilities

- `audio-capture`: 负责底层的麦克风录音控制、音频格式处理（16kHz PCM）。
- `hotkey-manager`: 负责全局热键的注册、监听和冲突处理。
- `stt-engine`: 负责与 STT 服务提供商（DashScope）的交互，处理鉴权和转录请求。
- `text-injection`: 负责将文本内容注入到操作系统当前的焦点窗口。
- `app-lifecycle`: 负责应用的启动、系统托盘管理、配置加载与持久化。

### Modified Capabilities

<!-- 这是一个新项目，没有现有的 Capability 需要修改 -->

## Impact

*   **系统依赖**：仅支持 Windows 10/11 (由于 WinMM 和 keyboard 库的依赖)。
*   **外部服务**：依赖 DashScope API 进行语音转文字（需要互联网连接）。
*   **权限**：应用需要管理员权限以注册全局钩子。

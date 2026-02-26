## Context

用户需要一个 Windows 平台的本地桌面应用 OpenType，实现“按住说话、松开上屏”的功能。该应用旨在提供极客友好的体验，同时具备完整的配置管理和系统托盘功能。参考项目 `opentypeless` 使用 Python 开发，依赖 WinMM 和 Keyboard 库。我们将沿用 Python 技术栈，并引入 PySide6 构建现代化 GUI。

## Goals / Non-Goals

**Goals:**
- 构建一个基于 Python + PySide6 的 Windows 桌面应用。
- 实现低延迟的音频捕获（WinMM）和全局热键响应（keyboard）。
- 集成 DashScope STT 服务，实现高准确率的中文语音转文字。
- 实现文本自动注入到任意焦点窗口。
- 提供系统托盘和配置界面，支持开机自启和参数调整。
- 遵循“极客友好、简洁高效”的设计原则。

**Non-Goals:**
- 跨平台支持（Mac/Linux 暂不考虑，专注于 Windows 体验）。
- 本地 STT 模型集成（虽然架构上预留接口，但本次仅实现 Cloud STT）。
- 复杂的音频编辑功能。

## Decisions

### 1. 技术栈选择：Python + PySide6
- **Decision**: 使用 Python 作为主要开发语言，PySide6 (Qt for Python) 作为 GUI 框架。
- **Rationale**:
    - Python 拥有丰富的 AI 和系统交互库（keyboard, pyaudio/winmm）。
    - PySide6 提供了原生外观的 UI 控件和强大的信号槽机制，适合构建响应式桌面应用。
    - 相比 Electron，Python 应用体积更小（虽然 PySide 也不小，但比 Chromium 内核小），且调用底层 API 更直接。
- **Alternatives**:
    - Electron: 资源占用较高，调用 Win32 API 需要编写 Node.js C++ 插件或使用 FFI，增加了复杂性。
    - Tauri: 性能极佳，但需要 Rust 知识，开发门槛较高，且 Python 生态的 AI 库无法直接复用。

### 2. 音频捕获：WinMM via `ctypes`
- **Decision**: 直接使用 `ctypes` 调用 Windows `winmm.dll` 进行录音。
- **Rationale**:
    - `opentypeless` 验证了该方案的可行性和低延迟特性。
    - 相比 `pyaudio` 或 `sounddevice`，直接调用 WinMM 可以减少第三方依赖，且更容易控制底层缓冲区，确保与 DashScope 的流式传输兼容。
    - 避免了 PortAudio 在 Windows 上可能出现的兼容性问题。

### 3. 全局热键：`keyboard` 库
- **Decision**: 使用 `keyboard` 库实现全局热键监听。
- **Rationale**:
    - `keyboard` 库在 Windows 上表现稳定，支持复杂的组合键。
    - 提供了底层的 Hook 机制，能够拦截和阻止按键事件传递（如果需要），实现“独占”热键体验。

### 4. 文本注入：模拟键盘输入
- **Decision**: 使用 `keyboard.write()` 或 `pyperclip` + `Ctrl+V` 模拟。
- **Rationale**:
    - 模拟键盘输入兼容性最好，适用于几乎所有 Windows 应用程序。
    - 对于长文本，`Ctrl+V` 速度更快，但会覆盖剪贴板。我们将优先尝试 `Ctrl+V` 方式，并在注入后恢复剪贴板内容（如果可能）。

### 5. 架构模式：MVC
- **Decision**: 采用 Model-View-Controller 模式。
    - **Model**: 处理业务逻辑（录音、STT、配置存储）。
    - **View**: PySide6 界面（设置窗口、托盘图标）。
    - **Controller**: 协调 Model 和 View，处理用户交互。
- **Rationale**: 分离关注点，便于维护和扩展。

## Risks / Trade-offs

- **Risk**: `keyboard` 库需要管理员权限。
    - **Mitigation**: 在应用启动时检测权限，如果非管理员运行，提示用户并尝试提权，或者在文档中明确说明。
- **Risk**: Cloud STT 延迟。
    - **Mitigation**: 使用流式 API (如果有) 或优化网络请求；提供视觉反馈（如托盘图标变化）告知用户正在处理。
- **Risk**: WinMM 兼容性。
    - **Mitigation**: 虽然 WinMM 是老旧 API，但在 Windows 10/11 上依然受支持且稳定。作为备选，可以封装一层 AudioInterface，未来替换为 WASAPI。

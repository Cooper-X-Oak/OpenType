## 1. Project Setup & Dependencies

- [x] 1.1 初始化 Python 虚拟环境并安装核心依赖 (PySide6, keyboard, requests, dashscope, pyaudio/winmm wrapper)。
- [x] 1.2 创建项目目录结构 (src/core, src/ui, src/utils, resources)。
- [x] 1.3 配置 logging 模块，建立基本的日志记录机制。

## 2. Core Modules Implementation

- [x] 2.1 实现 `AudioRecorder` 类：封装 WinMM API，支持 start/stop 录音，保存 PCM 数据。
- [x] 2.2 实现音频增益处理功能：计算 RMS 并标准化音量。
- [x] 2.3 实现 `STTEngine` 类：封装 DashScope API 调用，处理鉴权和网络请求。
- [x] 2.4 实现 `HotkeyManager` 类：使用 keyboard 库注册全局热键，管理按键事件回调。
- [x] 2.5 实现 `TextInjector` 类：封装文本注入逻辑 (Ctrl+V 模拟)。

## 3. UI Implementation (PySide6)

- [x] 3.1 创建主配置窗口 (`SettingsWindow`)：包含 API Key 输入、热键设置、录音设备选择等。
- [x] 3.2 实现系统托盘功能 (`SystemTray`)：支持最小化、右键菜单 (显示/退出)。
- [x] 3.3 实现配置持久化 (`ConfigManager`)：保存和加载用户设置 (config.json)。

## 4. Integration & Logic

- [x] 4.1 集成各模块到 `AppController`：连接热键事件 -> 录音 -> STT -> 注入 的完整流程。
- [x] 4.2 实现状态反馈：录音时托盘图标变化或显示悬浮提示。
- [x] 4.3 处理异常流程：网络错误提示、权限不足提示。

## 5. Packaging & Verification

- [x] 5.1 编写 E2E 测试脚本或手动验证清单，确保全流程可用。
- [x] 5.2 配置 PyInstaller 打包脚本，生成可执行文件 (.exe)。
- [x] 5.3 验证打包后的应用在无 Python 环境下能否正常运行。

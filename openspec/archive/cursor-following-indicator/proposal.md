## Why

为了追求极致的录音效率和体验，用户需要即时的视觉反馈，而不必将视线移至屏幕角落（托盘图标）。
目前的反馈机制（托盘图标变色）不够直观，且在高分屏或多屏环境下容易被忽略。
通过在光标附近显示一个随音量波动的动态指示器，可以提供明确的“正在录音”状态确认，增强用户的掌控感。

## What Changes

我们将实现一个 **光标跟随声纹指示器 (Cursor-Following Audio Visualizer)**：

*   **新增** `CursorIndicator` 组件 (UI)：
    *   一个无边框、背景透明、始终置顶的 PySide6 窗口。
    *   位置跟随鼠标光标（或在光标附近固定偏移）。
    *   绘制动态声纹（Waveform/Bar）以响应音量变化。
*   **修改** `AudioRecorder` (Core)：
    *   在录音回调中实时计算音频帧的 RMS（均方根）值。
    *   通过信号机制将归一化的音量数据发送给 UI 层。
*   **修改** `AppController` (Core)：
    *   管理 `CursorIndicator` 的生命周期（录音开始显示，结束隐藏）。
    *   连接 `AudioRecorder` 的数据流到 `CursorIndicator`。

## Capabilities

### New Capabilities

*   `ui-feedback`: 负责所有非标准窗口的视觉反馈（如光标指示器、Toast 提示等）。

### Modified Capabilities

*   `audio-capture`: 增加实时音量计算功能。

## Impact

*   **性能**：需要保证高频 UI 刷新（~30-60fps）不影响录音线程的稳定性。
*   **兼容性**：需确保在不同 DPI 设置和多显示器环境下，指示器位置准确且不被遮挡。
*   **交互**：指示器应“穿透”鼠标点击，避免干扰正常操作。

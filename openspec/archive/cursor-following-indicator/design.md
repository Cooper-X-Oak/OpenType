## Context

用户需要一个随光标移动的实时语音反馈指示器。当前录音时没有任何视觉反馈（除了托盘图标可能的变化），这导致用户无法确定录音是否正在进行，也无法判断音量是否合适。
该功能将实现一个类似 Typeless 但更轻量、更随身（Follow Cursor）的视觉反馈系统。

## Goals / Non-Goals

**Goals:**
- **光标跟随**: 指示器必须紧跟鼠标光标，或保持在光标附近的固定相对位置。
- **实时声纹**: 指示器内部必须显示实时的音量波形或能量条，以 30-60fps 刷新。
- **极低干扰**:
    - 无边框、背景透明。
    - 鼠标穿透（点击指示器区域应直接作用于下层窗口）。
    - 录音结束立即消失。
- **性能**: 音量计算和界面刷新不应阻塞主线程或录音线程。

**Non-Goals:**
- 复杂的音频可视化（如频谱图），仅实现简单的 RMS 能量显示。
- 自定义皮肤支持（第一版仅提供默认样式）。

## Decisions

### 1. UI 架构：PySide6 Overlay Window
- **Decision**: 使用 `QWidget` with `Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool`.
- **Transparency**: `setAttribute(Qt.WA_TranslucentBackground)` + `WA_TransparentForMouseEvents`.
- **Positioning**: 使用 `QTimer` 定时器（如 20ms）轮询 `QCursor.pos()` 并更新窗口位置。
    - *Alternative*: 使用 Windows Hook 监听鼠标移动事件。
    - *Rationale*: Hook 过于重且容易被杀软拦截，定时器轮询对于 UI 跟随来说足够平滑且实现简单。

### 2. 音量计算：RMS in Callback
- **Decision**: 在 `AudioRecorder` 的 PyAudio 回调中计算 RMS。
- **Formula**: `RMS = sqrt(sum(sample^2) / n)`。
- **Normalization**: 将 RMS 映射到 0.0 - 1.0 的线性范围，可能需要对数转换 (dB) 以符合人耳感知，但为简化第一版先用线性或简单的非线性映射。
- **Signal**: `AudioRecorder` 继承 `QObject`，通过 `Signal(float)` 发送音量值。

### 3. 数据流
- `AudioRecorder (Thread)` -> `emit signal` -> `AppController` -> `CursorIndicator.set_level(float)` -> `update()` -> `paintEvent`.

## Risks / Trade-offs

- **Risk**: `PyAudio` 回调是在 C 线程中运行，直接 emit PySide 信号可能导致崩溃或事件丢失。
    - **Mitigation**: PySide 的信号槽默认支持跨线程（QueuedConnection）。如果出现问题，可以使用 `QMetaObject.invokeMethod` 或中间队列。
- **Risk**: 频繁刷新 UI 导致 CPU 占用过高。
    - **Mitigation**: 限制刷新率（如 max 30fps），只有当音量变化超过阈值或位置改变时才重绘。

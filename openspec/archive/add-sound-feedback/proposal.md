# Change Proposal: add-sound-feedback

## Why
<!-- What problem are we solving? Why is this change necessary? -->
在之前的变更 `optimize-notifications` 中，我们为了减少视觉干扰，移除了大部分系统通知。
为了让用户在不看屏幕或不看托盘图标的情况下也能确认操作状态（开始录音、停止录音/成功识别、错误），我们需要引入非视觉的反馈机制。
音效反馈是一种极低干扰且高效的确认方式，符合“盲操作”的需求。

## What Changes
<!-- What will we build or modify? -->
引入轻量级的音效反馈系统，使用 Windows 原生 API (`winsound`) 播放简短的提示音。

具体场景与音效规划：
1.  **Start Recording**: 短促的高频音（如“哔”），提示录音开始。
2.  **Stop Recording / Success**: 短促的低频音或双音（如“哔-啵”），提示录音结束并开始处理。
3.  **Error**: 沉闷的错误音（如系统默认警告音），提示操作失败。

## Impact
<!-- Performance, security, or compatibility implications -->
*   **体验**: 补全了移除视觉通知后的反馈缺失，增强了操作的确定性。
*   **依赖**: 使用 Python 标准库 `winsound`，无需额外安装第三方库，保持轻量。
*   **性能**: `winsound.Beep` 或 `PlaySound` 均为异步或极低开销调用，不影响主线程性能。

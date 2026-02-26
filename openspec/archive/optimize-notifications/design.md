# Design: optimize-notifications

## Context
<!-- Background and current state -->
目前的 `AppController` 在多个状态下通过 `self.tray.showMessage` 发送系统通知。
- 录音过短：提示 "Recording too short."
- 未检测到语音：提示 "No speech detected."
- 成功识别：提示 "Input: {text}"
- 错误发生：提示错误信息。

这导致了“弹窗轰炸”。

## Goals / Non-Goals
<!-- What is in scope and what is out of scope? -->

**Goals:**
- **Silencing Success**: 成功识别并输入文字后，不显示任何系统通知。
- **Silencing Trivial Warnings**: 录音过短、未检测到语音等常规操作失误，不显示系统通知（因为已有光标指示器消失作为反馈，且用户知道自己没说话）。
- **Preserving Errors**: API 错误、设备故障等系统级错误仍需通知用户。

**Non-Goals:**
- 修改托盘图标的变化逻辑（那是另一种形式的反馈，需保留）。
- 修改日志记录逻辑（日志必须保留）。

## Design Decisions
<!-- Key technical decisions and rationale -->

### 1. 通知策略调整
| 事件 | 原行为 | 新行为 | 理由 |
| :--- | :--- | :--- | :--- |
| **Success** (Text recognized) | Show "Input: {text}" | **Remove** | 文字已上屏，无需重复确认。 |
| **Short Recording** (<0.1s) | Show "Recording too short" | **Remove** | 用户按错或反悔，无需打扰。 |
| **Silence** (No speech) | Show "No speech detected" | **Remove** | 可能是误触，静默处理更自然。 |
| **Error** (API/Device) | Show Error | **Keep** | 系统故障必须告知用户。 |

### 2. 代码修改点
- `src/core/app_controller.py`:
    - `process_audio`: 移除 `showMessage` 调用。
    - `on_processing_finished`: 移除 `showMessage` 调用。

## Risks / Trade-offs
<!-- Potential risks and mitigation strategies -->
- **Risk**: 用户可能不知道为什么没反应（比如麦克风坏了）。
- **Mitigation**: 真正的错误（如麦克风初始化失败）依然会弹窗。对于“没说话”这种情况，不反应是符合预期的（就像对空气说话一样）。

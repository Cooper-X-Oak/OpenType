# Change Proposal: optimize-notifications

## Why
<!-- What problem are we solving? Why is this change necessary? -->
用户反馈系统通知过多，造成干扰。
目前的逻辑是：无论录音成功、失败还是太短，都会弹出系统通知（Toast）。
特别是成功识别并输入文字后，依然会弹窗显示识别内容，这与“文字已上屏”形成了冗余信息，打断了用户的心流。

## What Changes
<!-- What will we build or modify? -->
优化通知策略，移除所有非必要的“成功”或“提示”类通知，仅保留关键错误通知。
具体包括：
1.  **移除** 成功识别后的内容弹窗。
2.  **移除** “录音太短”的警告弹窗（用户通常知道自己按快了）。
3.  **移除** “未检测到语音”的警告弹窗（静默失败即可）。
4.  **保留** 真正的系统错误弹窗（如 API 错误、设备错误）。

## Impact
<!-- Performance, security, or compatibility implications -->
*   **体验**: 大幅减少视觉干扰，实现“无感”交互。
*   **反馈**: 用户将主要依赖光标指示器（视觉）和即将加入的音效（听觉）来确认状态，而不是系统通知。

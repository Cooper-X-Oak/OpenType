# Design: optimize-cursor-indicator-position

## Context
<!-- Background and current state -->
目前的 `CursorIndicator` 位置偏移量为 `(x+15, y+15)`，用户反馈感觉“稍微离光标有点远”。
需要减小这个偏移量，使其更贴近光标，同时不遮挡光标本身。

## Goals / Non-Goals
<!-- What is in scope and what is out of scope? -->

**Goals:**
- 调整指示器位置，使其更靠近光标。
- 确保指示器不会遮挡鼠标光标的操作热点。

**Non-Goals:**
- 修改指示器的样式或颜色。
- 修改音量响应逻辑。

## Design Decisions
<!-- Key technical decisions and rationale -->

### 1. 偏移量调整
- **当前**: `x + 15, y + 15`
- **调整为**: `x + 10, y + 10` (或者更小，考虑到光标本身的大小)
- **Rationale**: 稍微减小偏移量，使其视觉上更紧凑。考虑到 Windows 默认光标大小约为 32x32 (但实际热点在左上角，视觉主体约 10-15px)，`+10` 是一个比较安全的贴近距离。

## Risks / Trade-offs
<!-- Potential risks and mitigation strategies -->
- **Risk**: 距离太近导致指示器与光标重叠，影响视觉。
- **Mitigation**: 保持至少 10px 的偏移，确保不重叠。

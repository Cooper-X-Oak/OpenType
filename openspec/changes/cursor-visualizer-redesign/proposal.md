# Cursor Visualizer Redesign Proposal

## 背景 (Background)
目前的视觉图标（绿色条状）被认为不够美观。用户希望将其重新设计为一个更加符合“Geek”和“Cyberpunk”风格的视觉元素。

## 目标 (Goals)
1.  **形态重构**：将图标形状改为竖向的椭圆状。
2.  **色彩基调**：采用黑白色调作为容器/背景。
3.  **声纹可视化**：内部展示随音量变化的声纹线条。
4.  **风格化**：线条呈现赛博朋克风格（如荧光绿色）。

## 范围 (Scope)
-   修改 `src/ui/cursor_indicator.py` 中的 `CursorIndicator` 类。
-   更新绘制逻辑（`paintEvent`）。
-   移除旧的矩形条状绘制逻辑。

## 成功标准 (Success Criteria)
-   图标呈现为竖向椭圆，背景黑白，内部有荧光绿声纹。
-   声纹随麦克风音量实时跳动，流畅无卡顿。
-   符合用户对“丑”的改进期望。

# Cursor Visualizer Redesign Design

## 1. 视觉设计 (Visual Design)

### 1.1 容器 (Container)
- **形状**: 竖向胶囊/椭圆 (Vertical Capsule/Oval)。
- **尺寸**: 宽度固定约 14px，高度固定约 32px (保持小巧，不遮挡视线)。
- **背景**: 纯黑 (`#000000`)，不透明度 90% (保留一丝通透感)。
- **边框**: 白色 (`#FFFFFF`) 或 浅灰 (`#EEEEEE`)，线宽 1px，增强轮廓感。

### 1.2 核心元素：声纹 (Voice Waveform)
- **风格**: 类似“心电图 (EKG)”或“示波器 (Oscilloscope)”的折线风格。
- **颜色**: 赛博朋克荧光绿 (Cyberpunk Neon Green, e.g., `#00FF41` 或 `#39FF14`)。
- **形态**:
  - 采用 **竖向波形** (Vertical Waveform)。
  - 就像一根竖直绷紧的弦，随着音量震动。
  - 静默时：一条笔直的竖线（或微微噪点抖动）。
  - 说话时：线条在水平方向左右震荡，振幅随音量 `self.level` 变化。

## 2. 技术实现 (Technical Implementation)

### 2.1 类修改 (`CursorIndicator`)
- **继承**: 保持 `QWidget`，无边框，置顶。
- **状态管理**:
  - 新增 `self.wave_history` (Deque): 存储最近 N 帧的振幅偏移量，用于绘制连续折线（可选，或者简单实用随机噪点+正弦波合成）。
  - 简化方案：每一帧生成一条新的随机折线路径 (Randomized Polyline)，因为人声变化极快，不需要像心电图那样严谨的“滚动”效果，**实时震动**视觉效果更佳且性能更好。

### 2.2 绘制逻辑 (`paintEvent`)
1.  **绘制背景**:
    - `painter.setBrush(Qt.black)`
    - `painter.setPen(Qt.white)`
    - `painter.drawRoundedRect(..., w/2, w/2)` (全圆角)
2.  **计算波形**:
    - 设定节点数：例如垂直方向取 5-8 个点。
    - Y坐标：均匀分布。
    - X坐标：`Center_X + Random(-1, 1) * Amplitude * Level`。
    - 顶部和底部点固定在中心，确保线条“绷紧”。
3.  **绘制线条**:
    - `painter.setPen(NeonGreen, width=1.5)`
    - `painter.drawPolyline(points)`

## 3. 性能评估 (Performance Review)
- **复杂度**: O(N)，N 为波形点数 (Is very small, <10)。
- **渲染**: 纯矢量绘制，GPU 占用极低。
- **内存**: 几乎无额外内存占用。

## 4. 影响分析 (Impact Analysis)
- **体积**: 代码增量 < 1KB。无资源文件。
- **现有功能**: 仅替换 `paintEvent` 和尺寸定义，不影响热键或录音逻辑。

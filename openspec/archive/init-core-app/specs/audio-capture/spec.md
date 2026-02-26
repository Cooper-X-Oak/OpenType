## ADDED Requirements

### Requirement: 音频录制控制
系统必须支持通过 WinMM API 进行低延迟的音频录制。录音参数应固定为 16kHz 采样率、单声道、16位深度 (PCM)，以适配大多数 STT 模型的输入要求。

#### Scenario: 开始录音
- **GIVEN** 用户按下配置的热键
- **WHEN** 触发录音开始指令
- **THEN** 系统立即初始化 WinMM 设备并开始捕获音频流
- **AND** 录音状态标记为 "Recording"

#### Scenario: 停止录音
- **GIVEN** 系统正在录音中
- **WHEN** 用户松开热键
- **THEN** 系统立即停止音频捕获
- **AND** 将捕获的音频数据保存为临时 WAV 文件或内存对象
- **AND** 录音状态标记为 "Stopped"

### Requirement: 录音音量增益
系统应在录音结束后自动对音频数据进行标准化处理，以确保音量水平适合 STT 识别（目标 RMS 8000）。

#### Scenario: 音频增益处理
- **GIVEN** 录音已完成
- **WHEN** 音频数据被传递给处理模块
- **THEN** 系统计算当前音频的 RMS
- **AND** 应用增益使得 RMS 接近目标值

## ADDED Requirements

### Requirement: Cloud STT 集成 (DashScope)
系统必须支持接入 DashScope (通义千问) 的语音识别服务。

#### Scenario: 提交识别请求
- **GIVEN** 音频录制完成且数据已处理
- **WHEN** 音频数据被传递给 STT 引擎
- **THEN** 系统构建符合 DashScope API 规范的 HTTP/WebSocket 请求
- **AND** 使用配置的 API Key 进行鉴权

#### Scenario: 接收识别结果
- **GIVEN** 识别请求已发送
- **WHEN** API 返回 JSON 响应
- **THEN** 系统解析响应内容，提取识别出的文本
- **AND** 触发“识别成功”事件，将文本传递给注入模块

### Requirement: 错误处理
系统必须能够优雅地处理 STT 服务的错误，如网络超时、API Key 无效或配额不足。

#### Scenario: 网络超时
- **GIVEN** 网络连接不稳定
- **WHEN** STT 请求超时（如超过 10 秒）
- **THEN** 系统中止请求
- **AND** 触发“识别失败”事件，并记录错误日志
- **AND** 提示用户检查网络连接

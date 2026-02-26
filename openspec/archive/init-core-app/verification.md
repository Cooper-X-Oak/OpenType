# 验证清单 (Verification Checklist)

## 1. 环境准备

- [ ] 确保已安装 Python 3.10+
- [ ] 确保已安装依赖: `pip install -r requirements.txt`
- [ ] 获取 DashScope API Key

## 2. 功能验证

### 2.1 启动与配置
- [ ] 运行 `python src/main.py` 或 `dist/OpenType.exe`
- [ ] 检查系统托盘是否出现 OpenType 图标 (灰色/Idle)
- [ ] 双击托盘图标，打开设置窗口
- [ ] 输入 DashScope API Key
- [ ] 设置热键 (默认 F2)
- [ ] 点击 Save 保存，检查 `config.json` 是否更新

### 2.2 录音与识别
- [ ] 按住热键 (F2)，观察托盘图标变为红色 (Recording)
- [ ] 说话 (e.g. "你好，世界")
- [ ] 松开热键，观察托盘图标变回灰色
- [ ] 等待几秒，检查当前活动窗口 (如记事本) 是否输入了识别的文本
- [ ] 检查日志 `logs/OpenType_YYYYMMDD.log` 是否有 "Recognized: ..."

### 2.3 异常处理
- [ ] 拔掉麦克风或禁用录音设备，尝试录音，检查是否提示错误
- [ ] 断开网络，尝试识别，检查是否提示网络/API错误
- [ ] 设置无效的 API Key，检查是否提示认证失败

### 2.4 系统托盘
- [ ] 右键点击托盘图标
- [ ] 点击 "Settings" 打开设置窗口
- [ ] 点击 "Exit" 退出程序

## 3. 打包验证

- [ ] 运行 `python scripts/build.py`
- [ ] 检查 `dist/OpenType.exe` 是否生成
- [ ] 在无 Python 环境 (或仅运行 exe) 下重复上述 2.1 - 2.4 测试

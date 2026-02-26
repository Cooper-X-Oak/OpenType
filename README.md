# OpenType 🎙️

**OpenType** 是一个为 Windows 打造的极简、无界面（Typeless）语音输入工具。它专为极客设计，通过全局热键和云端大模型（DashScope），将语音实时转换为文字并自动输入到当前光标位置。

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 特性

- **全局热键控制**: 默认 `F2` 一键录音，再次按下停止并识别。
- **云端高精度识别**: 集成阿里云 DashScope (Paraformer-Realtime) 模型，识别准确率远超本地离线模型。
- **无感输入**: 识别完成后，自动模拟键盘输入将文字“粘贴”到当前焦点窗口。
- **极简设计**: 仅在系统托盘运行，无干扰界面，资源占用低。
- **音频增益**: 自动处理录音音量，确保识别效果。
- **完全可配置**: 支持自定义 API Key、热键、音频设备等。

## 🚀 快速开始

### 1. 获取程序
前往 [Releases](../../releases) 页面下载最新版本的 `OpenType-vX.X.X.zip`。

### 2. 配置 API Key
解压后，在 `OpenType.exe` 同级目录下创建或修改 `config.json` 文件：

```json
{
    "api_key": "YOUR_DASHSCOPE_API_KEY",
    "hotkey": "f2",
    "audio_device_index": null,
    "target_dbfs": -20.0
}
```

> **注意**: 你需要先在阿里云 DashScope 申请一个 API Key。

### 3. 运行使用
1. 双击运行 `OpenType.exe`。
2. 可以在系统托盘看到一个灰色的圆点图标（表示空闲）。
3. 在任意文本输入框中（如记事本、微信、VS Code），按下 `F2` 开始说话（图标变红）。
4. 说完后再次按下 `F2`。
5. 等待片刻，文字将自动输入到光标处。

## 🛠️ 本地开发

如果你想参与开发或自己构建：

### 环境要求
- Windows 10/11
- Python 3.12+

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 运行源码

```bash
# 设置 PYTHONPATH (如果需要)
$env:PYTHONPATH="src"

# 启动
python src/main.py
```

### 打包发布

```bash
python scripts/build.py
```
构建产物将生成在 `dist/` 和 `releases/` 目录。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源。

# Design: add-sound-feedback

## Context
<!-- Background and current state -->
用户希望在进行录音操作时有轻微的反馈，但不希望是视觉上的弹窗。
目前 `AppController` 通过 `recording_started` / `recording_stopped` 信号控制托盘图标变化，但没有声音。

## Goals / Non-Goals
<!-- What is in scope and what is out of scope? -->

**Goals:**
- **Auditory Feedback**: 在开始录音、结束录音、发生错误时播放声音。
- **Lightweight**: 使用 Windows 内置声音 API (`winsound`)，避免引入大型音频库。
- **Non-blocking**: 播放声音不应阻塞主线程或 UI 响应。

**Non-Goals:**
- 自定义复杂的 WAV 音频文件（先使用 `winsound.Beep` 生成简单的频率音，或使用系统提示音）。
- 可配置的音效库（暂不支持上传自定义音效，只做最基础的开关或预设）。

## Design Decisions
<!-- Key technical decisions and rationale -->

### 1. 技术选型
使用 Python 标准库 `winsound` (仅限 Windows)。
- `winsound.Beep(frequency, duration)`: 可以生成特定频率的蜂鸣声，非常有极客感 (Geeky)，且不需要任何外部文件。
- `winsound.PlaySound(sound, flags)`: 可以播放系统预设声音（如 `SystemExclamation`）。

**决策**: 采用 `winsound.Beep` 生成独特的极客风格提示音。
- **Start**: 高频短音 (e.g., 800Hz, 100ms) -> "滴"
- **Stop**: 低频短音 (e.g., 400Hz, 100ms) -> "嘟"
- **Error**: 连续短促低音 (e.g., 200Hz, 100ms * 2) -> "嘟嘟"

### 2. 异步播放
`winsound.Beep` 是阻塞调用的。为了不卡顿 UI，必须在独立线程中播放。
我们可以封装一个简单的 `SoundManager` 或直接在 `AppController` 中使用 `threading.Thread` 包装播放逻辑。

### 3. 代码结构
新增 `src/utils/sound_player.py`:
```python
import winsound
import threading

def play_beep(freq, duration):
    threading.Thread(target=winsound.Beep, args=(freq, duration), daemon=True).start()

def play_start_sound():
    play_beep(800, 150)

def play_stop_sound():
    play_beep(400, 150)

def play_error_sound():
    # play_beep(200, 300)
    threading.Thread(target=winsound.MessageBeep, args=(winsound.MB_ICONHAND,), daemon=True).start()
```

集成到 `AppController`:
- `start_recording` -> `play_start_sound()`
- `stop_and_process` -> `play_stop_sound()`
- `error_occurred` -> `play_error_sound()`

## Risks / Trade-offs
<!-- Potential risks and mitigation strategies -->
- **Risk**: 声音过于刺耳或打扰旁人。
- **Mitigation**: 频率和时长需要调教，尽量短促柔和。后续可以添加静音开关。

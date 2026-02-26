# Tasks

- [x] **Modify AudioRecorder** <!-- id: 0 -->
  - [x] Make `AudioRecorder` inherit from `QObject` (PySide6.QtCore).
  - [x] Add `audio_level_changed = Signal(float)` signal.
  - [x] Implement RMS calculation in `_callback` method using `numpy` or `audioop` (use standard lib or numpy if available).
  - [x] Emit normalized audio level (0.0-1.0) via signal.
  - [x] Ensure thread safety for signal emission from callback.

- [x] **Create CursorIndicator** <!-- id: 1 -->
  - [x] Create `src/ui/cursor_indicator.py`.
  - [x] Implement `CursorIndicator(QWidget)` class.
  - [x] Configure window flags: `FramelessWindowHint`, `WindowStaysOnTopHint`, `Tool`.
  - [x] Configure attributes: `WA_TranslucentBackground`, `WA_TransparentForMouseEvents`.
  - [x] Implement `set_level(float)` slot to update internal state and trigger repaint.
  - [x] Implement `paintEvent` to draw a dynamic visual (e.g., expanding circle or bar).
  - [x] Implement `update_position()` method to follow `QCursor.pos()` with an offset.
  - [x] Add a `QTimer` for smooth position updates (e.g., 20ms interval).

- [x] **Integrate in AppController** <!-- id: 2 -->
  - [x] Import `CursorIndicator` in `src/core/app_controller.py`.
  - [x] Instantiate `self.cursor_indicator` in `__init__`.
  - [x] Connect `self.recorder.audio_level_changed` to `self.cursor_indicator.set_level`.
  - [x] In `start_recording`: `self.cursor_indicator.show()`, start position timer.
  - [x] In `stop_recording`: `self.cursor_indicator.hide()`, stop position timer.

- [x] **Verification** <!-- id: 3 -->
  - [x] Run the application.
  - [x] Trigger recording (Hotkey).
  - [x] Verify indicator appears near cursor.
  - [x] Speak into microphone and verify visual feedback responds to volume.
  - [x] Verify indicator disappears after recording stops.
  - [x] Verify no errors in console/logs.

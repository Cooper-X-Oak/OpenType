# Tasks

- [x] **Create Sound Utilities** <!-- id: 0 -->
  - [x] Create `src/utils/sound_player.py`.
  - [x] Implement `play_beep` (async wrapper for `winsound.Beep`).
  - [x] Implement `play_start_sound`, `play_stop_sound`, `play_error_sound`.

- [x] **Integrate into AppController** <!-- id: 1 -->
  - [x] Import `src/utils/sound_player` in `src/core/app_controller.py`.
  - [x] Call `play_start_sound()` in `start_recording`.
  - [x] Call `play_stop_sound()` in `stop_and_process`.
  - [x] Call `play_error_sound()` in `error_occurred` or `show_error`.

- [x] **Verify Sounds** <!-- id: 2 -->
  - [x] Run application.
  - [x] Test recording start -> Hear "beep".
  - [x] Test recording stop -> Hear "boop".
  - [x] Test error -> Hear error sound.

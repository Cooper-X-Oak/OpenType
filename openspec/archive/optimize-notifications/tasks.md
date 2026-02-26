# Tasks

- [x] **Silence Success Notifications** <!-- id: 0 -->
  - [x] Remove `self.tray.showMessage` in `AppController.on_processing_finished`.

- [x] **Silence Trivial Warnings** <!-- id: 1 -->
  - [x] Remove `self.tray.showMessage` in `AppController.process_audio` for "Recording too short".
  - [x] Remove `self.tray.showMessage` in `AppController.process_audio` for "No speech detected".

- [x] **Verification** <!-- id: 2 -->
  - [x] Run application.
  - [x] Perform a successful recording -> Verify no system notification.
  - [x] Perform a very short click -> Verify no system notification.
  - [x] Perform a silent recording -> Verify no system notification.
  - [x] Force an error (e.g. invalid API key) -> Verify error notification still appears.

# Refine Geek UI Design

## Visual Concept
-   **Metaphor**: A "Retro Terminal Cursor" or "Command Prompt".
-   **Shape**: A solid block that transforms.
    -   **Idle State**: A low-profile "Underscore" cursor (`_`), indicating "Waiting for input".
    -   **Active State**: Expands vertically into a full "Block" cursor (`█`) based on voice volume.
-   **Color**:
    -   Primary: Terminal Green (`#00FF00`) or Hacker Green (`#0F0`).
    -   Secondary (Loud): Slightly brighter or white core.
-   **Animation**:
    -   Smooth transition between Underscore and Block height.
    -   Subtle "CRT Scanline" or "Glow" effect for that retro feel.

## Implementation Details
### `src/ui/cursor_indicator.py`
-   **Geometry**:
    -   Base size: 20x30px (narrow vertical rectangle).
    -   Position: Offset `-10, -20` (to sit right next to/above text cursor).
-   **Paint Logic**:
    -   Draw a fixed-width rectangle.
    -   Height = `base_height + (max_height - base_height) * level`.
    -   Color = `QColor(0, 255, 0, alpha)`.
    -   Add a faint shadow/glow for contrast on white backgrounds.

## User Experience
-   **Minimal Intrusion**: Takes up very little horizontal space.
-   **Clear Feedback**: Vertical expansion clearly shows "I hear you".
-   **Cool Factor**: Feels like the system is "listening" in a raw, code-centric way.

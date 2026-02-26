# Refine Geek UI Proposal

## Background
User wants a "Geek", "Modern", "Minimalist" UI style that takes up less resource/screen space.
The current implementation (blue circle with gradient glow) feels a bit "generic OS" and less "Hacker/Terminal".
The goal is to align with the "Geek Persona" & "Hackathon Goal" (Core Memory).

## Goals
1.  **Visual Style**: Switch to a Terminal/Retro-Futuristic aesthetic.
2.  **Minimalism**: Reduce visual clutter.
3.  **Responsiveness**: Maintain high performance and low resource usage.

## Scope
-   Modify `src/ui/cursor_indicator.py`.
-   Update `CursorIndicator` class to render a new style.
-   Remove old "glow" effect if it conflicts with the new style.

## Success Criteria
-   User feels the new UI is "Cool" and "Geeky".
-   Indicator is clearly visible but not distracting.
-   Animation is smooth (60fps).

"""
state_manager.py — Stack-based screen/view state machine.

Each screen implements:
    on_enter(manager, **kwargs)  — called when pushed/switched
    on_exit(manager)             — called when popped/replaced
    handle_event(event)          — pygame event processing
    update(dt)                   — logic tick (dt in seconds)
    draw(surface)                — render to surface
"""


class StateManager:
    def __init__(self):
        self._stack: list = []
        self.running: bool = True
        # Shared game state accessible to all screens
        self.game_state: dict = {}

    # ─── Stack operations ──────────────────────────────────────────────────────

    def push(self, screen, **kwargs):
        """Push a new screen onto the stack (old screen stays beneath)."""
        if self._stack:
            self._stack[-1].on_exit(self)
        self._stack.append(screen)
        screen.on_enter(self, **kwargs)

    def pop(self):
        """Remove the top screen; resume the one beneath it."""
        if self._stack:
            self._stack[-1].on_exit(self)
            self._stack.pop()
        if self._stack:
            self._stack[-1].on_enter(self)

    def switch(self, screen, **kwargs):
        """Replace the top screen (pop + push without keeping old screen)."""
        if self._stack:
            self._stack[-1].on_exit(self)
            self._stack.pop()
        self._stack.append(screen)
        screen.on_enter(self, **kwargs)

    def replace_all(self, screen, **kwargs):
        """Clear the entire stack and start fresh with screen."""
        while self._stack:
            self._stack[-1].on_exit(self)
            self._stack.pop()
        self._stack.append(screen)
        screen.on_enter(self, **kwargs)

    def quit(self):
        self.running = False

    # ─── Main loop delegation ─────────────────────────────────────────────────

    def handle_event(self, event):
        if self._stack:
            self._stack[-1].handle_event(event)

    def update(self, dt: float):
        if self._stack:
            self._stack[-1].update(dt)

    def draw(self, surface):
        # Draw all screens (bottom up) so overlays work
        for screen in self._stack:
            screen.draw(surface)

    @property
    def current(self):
        return self._stack[-1] if self._stack else None


class BaseScreen:
    """Convenience base class — all methods no-op by default."""

    def on_enter(self, manager, **kwargs):
        pass

    def on_exit(self, manager):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface):
        pass

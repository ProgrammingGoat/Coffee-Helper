import asyncio
import time

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class Timer(toga.Box):
    """Class that represents a timer module with a progress bar and a countdown."""

    def __init__(self, app: toga.App, duration_in_seconds: int):
        """Constructs a new timer.

        Parameters
        ----------
        app: toga.App
            the app the Timer belongs to. This is required for access to the event loop.
        duration_in_seconds: int
            the duration the timer is supposed to run.
        """
        super().__init__(style=Pack(direction=COLUMN, flex=1))
        self.app = app
        self.duration = duration_in_seconds
        self.pause_progress = 0
        self.setup()

    def setup(self):
        """Generates the UI."""
        timer_row = toga.Box(style=Pack(direction=ROW, flex=1))
        self.progress_bar = toga.ProgressBar(
            max=self.duration, value=0, style=Pack(flex=1)
        )

        self.start_button = toga.Button("Start", on_press=self.start)
        self.pause_button = toga.Button("Pause", enabled=False)

        timer_row.add(self.progress_bar, self.start_button, self.pause_button)
        self.add(timer_row)

        self.label = toga.Label(
            f"Time: {self.duration // 60:02d}:{self.duration % 60:02d}"
        )
        self.add(self.label)

    def update_ui(self, time):
        """Updates the progress bar and time display with the remaining time once each tick."""

        self.progress_bar.value = time
        time_remaining = int(self.duration - time)
        self.label.text = f"Time: {time_remaining // 60:02d}:{time_remaining % 60:02d}"

    def start(self, widget=None):
        """Starts the timer."""

        self.start_button.text = "Cancel"
        self.start_button.on_press = self.abort

        self.pause_button.text = "Pause"
        self.pause_button.on_press = self.pause
        self.pause_button.enabled = True
        self.pause_button.focus()

        self.progress_bar.start()
        self.start_time = time.time()
        self.is_running = True
        self.app.add_background_task(self.tick_timer)

    def stop(self, widget=None):
        """Stops the timer."""

        self.start_button.text = "Start"
        self.start_button.on_press = self.start
        self.pause_button.enabled = False

        self.is_running = False
        self.progress_bar.stop()

    def pause(self, widget=None):
        """Pauses the timer and saves the current progress."""

        self.pause_button.text = "Resume"
        self.pause_button.on_press = self.resume

        self.is_running = False
        self.pause_progress = time.time() - self.start_time
        self.progress_bar.stop()

    def resume(self, widget=None):
        """Resumes the timer where it was left off."""

        self.pause_button.text = "Pause"
        self.pause_button.on_press = self.pause

        self.is_running = True
        self.start_time = time.time() - self.pause_progress
        self.app.add_background_task(self.tick_timer)

    def abort(self, widget=None):
        """Cancels the timer and resets it."""

        self.update_ui(0)
        self.stop()

    def finish(self, widget=None):
        """Stops the timer and ensures the progress bar is fully filled."""

        self.progress_bar.value = self.duration
        self.app.beep()
        self.stop()

    async def tick_timer(self, app):
        """Coroutine that gets added to the app's main event loop.
        Twice a second, it checks how much time has passed since the timer has started.
        If enough time has passed for the timer to finish, the finish method is called.
        Otherwise, updates the UI with the current remaining time and asks the event loop to return in half a second."""

        while self.is_running:
            delta = time.time() - self.start_time
            if delta >= self.duration:
                self.finish()
                return

            self.update_ui(delta)
            print("tick")
            # asynchronous sleep to prevent blocking the UI
            await asyncio.sleep(0.5)

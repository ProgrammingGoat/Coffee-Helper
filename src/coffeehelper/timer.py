import asyncio
import time
import toga

from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Timer(toga.Box):
    def __init__(self, app: toga.App, duration_in_seconds: int):
        super().__init__(style=Pack(direction=COLUMN, flex=1))
        self.app = app
        self.duration = duration_in_seconds
        self.pause_progress = 0
        self.setup()

    def setup(self):
        timer_row = toga.Box(style=Pack(direction=ROW, flex=1))
        self.progress_bar = toga.ProgressBar(
            max=self.duration, 
            value=0,
            style=Pack(flex=1))
        
        self.start_button = toga.Button("Start", on_press=self.start)
        self.pause_button = toga.Button("Pause", enabled=False)
        
        timer_row.add(self.progress_bar, self.start_button, self.pause_button)
        self.add(timer_row)

        self.label = toga.Label(f"Time: {self.duration // 60:02d}:{self.duration % 60:02d}")
        self.add(self.label)

    def update_ui(self, time):
        self.progress_bar.value = time
        time_remaining = int(self.duration - time)
        self.label.text = f"Time: {time_remaining // 60:02d}:{time_remaining % 60:02d}"
    
    def start(self, widget=None):
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
        self.start_button.text = "Start"
        self.start_button.on_press = self.start
        self.pause_button.enabled = False

        self.is_running = False
        self.progress_bar.stop()

    def pause(self, widget=None):
        self.pause_button.text = "Resume"
        self.pause_button.on_press = self.resume

        self.is_running = False
        self.pause_progress = time.time() - self.start_time
        self.progress_bar.stop()

    def resume(self, widget=None):
        self.pause_button.text = "Pause"
        self.pause_button.on_press = self.pause

        self.is_running = True
        self.start_time = time.time() - self.pause_progress
        self.app.add_background_task(self.tick_timer)

    def abort(self, widget=None):
        self.update_ui(0)
        self.stop()

    def finish(self, widget=None):
        self.progress_bar.value = self.duration
        self.app.beep()

    async def tick_timer(self, app):
        while self.is_running:
            delta = time.time() - self.start_time
            if delta >= self.duration:
                self.finish()
                return

            self.update_ui(delta)
            await asyncio.sleep(0.5)
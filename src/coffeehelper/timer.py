import asyncio
import time
import toga

from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Timer(toga.Box):
    def __init__(self, app: toga.App, duration: int):
        super().__init__(style=Pack(direction=COLUMN, flex=1))
        self.app = app
        self.duration = duration
        self.setup()

    def setup(self):
        self.progress_bar = toga.ProgressBar(
            max=self.duration, 
            value=0,
            style=Pack(flex=1))
        self.add(self.progress_bar)

        self.label = toga.Label(f"Time: {self.duration // 60:02d}:{self.duration % 60:02d}")
        self.add(self.label)

    def update_ui(self, time):
        self.progress_bar.value = time
        time_remaining = int(self.duration - time)
        self.label.text = f"Time: {time_remaining // 60:02d}:{time_remaining % 60:02d}"
    
    def start(self):
        self.progress_bar.start()
        self.start_time = time.time()
        self.timer_is_running = True
        self.app.add_background_task(self.tick_timer)
    
    def stop(self):
        self.progress_bar.value = self.duration
        self.progress_bar.stop()
        self.app.beep()

    async def tick_timer(self, app):
        while self.timer_is_running:
            delta = time.time() - self.start_time
            if delta >= self.duration:
                self.stop()
                return

            self.update_ui(delta)
            await asyncio.sleep(0.5)
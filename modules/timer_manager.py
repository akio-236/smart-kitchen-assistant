import threading
import time
from datetime import datetime


class TimerManager:
    def __init__(self):
        self.active_timers = []

    def add_timer(self, duration, message):
        timer = {
            "start_time": datetime.now(),
            "duration": duration,
            "message": message,
            "completed": False,
        }
        self.active_timers.append(timer)

        thread = threading.Thread(target=self._monitor_timer, args=(timer,))
        thread.daemon = True
        thread.start()

    def _monitor_timer(self, timer):
        end_time = timer["start_time"].timestamp() + timer["duration"]
        while time.time() < end_time:
            time.sleep(0.1)
        timer["completed"] = True
        print(f"ALARM: {timer['message']}")

    def get_active_timers(self):
        active = []
        for timer in self.active_timers:
            if not timer["completed"]:
                elapsed = (datetime.now() - timer["start_time"]).total_seconds()
                remaining = max(0, timer["duration"] - elapsed)
                mins, secs = divmod(int(remaining), 60)
                active.append(
                    {"message": timer["message"], "remaining": f"{mins}m {secs}s"}
                )
        return active

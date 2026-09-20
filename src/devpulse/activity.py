import time

import pywinctl as pwc

from devpulse.decorators import start_times_tamp


@start_times_tamp
def get_active_window_title():
    active_window = pwc.getActiveWindow()
    if active_window:
        return active_window
    else:
        return None


previous_window = None
previous_start_time = None

while True:
    current_window, observed_at = get_active_window_title()

    if current_window and current_window != previous_window:
        print(
            f"Focused window title changed: {current_window.title} at {observed_at}")
        if previous_window and previous_start_time:
            print(f"""
            Session ended
            Application: {previous_window.getAppName()}
            Window: {previous_window.title}
            Window Handle: {previous_window.getHandle()}
            PID: {previous_window.getPID()}
            Start time: {previous_start_time}
            End time: {observed_at}
            Duration: {observed_at - previous_start_time}
            """)
        previous_window = current_window
        previous_start_time = observed_at

    time.sleep(0.25)

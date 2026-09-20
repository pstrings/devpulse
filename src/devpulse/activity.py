import time

import pywinctl as pwc

from devpulse.decorators import start_time_stamp


@start_time_stamp
def get_active_window():
    active_window = pwc.getActiveWindow()
    if active_window:
        return active_window
    else:
        return None


previous_title = None
previous_handle = None
previous_app_name = None
previous_pid = None
previous_start_time = None
session = []

try:
    while True:
        current_window, observed_at = get_active_window()
        current_title = current_window.title if current_window else None
        current_handle = current_window.getHandle() if current_window else None
        current_pid = current_window.getPID() if current_window else None
        current_app_name = current_window.getAppName() if current_window else None

        if current_title and (current_handle != previous_handle or current_title != previous_title):
            if previous_title and previous_start_time:
                session.append({
                    "application": previous_app_name,
                    "pid": previous_pid,
                    "window_handle": previous_handle,
                    "window_title": previous_title,
                    "start_time": previous_start_time,
                    "end_time": observed_at,
                    "duration": observed_at - previous_start_time
                })

            print(
                f"Focused window title changed: {current_window.title} at {observed_at}")

            previous_title = current_title
            previous_handle = current_handle
            previous_pid = current_pid
            previous_app_name = current_app_name
            previous_start_time = observed_at

        time.sleep(0.25)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    print(session)

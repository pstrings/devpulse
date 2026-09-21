import time
from pprint import pp

import pywinctl as pwc

from devpulse.decorators import start_time_stamp
from devpulse.models import ActivitySession


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
observed_at = None
session = []


def create_active_session(application, pid, window_handle, window_title, start_time, end_time):
    session.append(ActivitySession(
        application=application,
        pid=pid,
        window_handle=window_handle,
        window_title=window_title,
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time
    ))


try:
    while True:
        current_window, observed_at = get_active_window()
        current_title = current_window.title if current_window else None
        current_handle = current_window.getHandle() if current_window else None
        current_pid = current_window.getPID() if current_window else None
        current_app_name = current_window.getAppName() if current_window else None

        if current_title and (current_handle != previous_handle or current_title != previous_title):
            if previous_title and previous_start_time and previous_handle and previous_pid and previous_app_name:
                create_active_session(
                    application=previous_app_name,
                    pid=previous_pid,
                    window_handle=previous_handle,
                    window_title=previous_title,
                    start_time=previous_start_time,
                    end_time=observed_at
                )

            print(
                f"Focused window title changed: {current_window.title} at {observed_at}")

            previous_title = current_title
            previous_handle = current_handle
            previous_pid = current_pid
            previous_app_name = current_app_name
            previous_start_time = observed_at

        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if previous_title and previous_start_time and previous_handle and previous_pid and previous_app_name and observed_at:
        create_active_session(
            application=previous_app_name,
            pid=previous_pid,
            window_handle=previous_handle,
            window_title=previous_title,
            start_time=previous_start_time,
            end_time=observed_at
        )
    pp(session)

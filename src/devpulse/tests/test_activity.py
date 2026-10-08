from datetime import UTC, datetime, timedelta

import pandas as pd

from devpulse.analytics.activity import (
    add_productivity_metrics,
    analyze_sessions,
    calculate_application_stats,
)
from devpulse.models import ActivitySessionData


def test_calculate_application_stats():
    df = pd.DataFrame(
        {
            "application": [
                "Code.exe",
                "Code.exe",
                "brave.exe",
                "vstudio.exe"
            ],
            "duration": [
                10.0,
                20.0,
                30.0,
                40.0
            ]
        }
    )

    result = calculate_application_stats(df)

    code = result[result["application"] == "Code.exe"].iloc[0]

    assert code["total_duration"] == 30.0
    assert code["session_count"] == 2
    assert code["total_minutes"] == 0.5
    assert code["avg_session_duration"] == 15.0
    assert code["percentage"] == 30.0


def test_add_productivity_metrics():
    df = pd.DataFrame(
        {
            "application": [
                "Code.exe",
                "brave.exe",
                "vstudio.exe",
            ],
            "duration": [
                60.0,
                30.0,
                10.0,
            ],
        }
    )

    result = add_productivity_metrics(df)

    assert result["is_productive"].tolist() == [True, False, True]
    assert result["productive_percentage"].iloc[0] == 70.0


def test_analyze_sessions():
    sessions = [
        ActivitySessionData(
            application="Code.exe",
            pid=100,
            window_handle=200,
            window_title="activity.py",
            start_time=datetime(2026, 10, 3, 16, 0, tzinfo=UTC),
            end_time=datetime(2026, 10, 3, 16, 10, tzinfo=UTC),
            duration=timedelta(minutes=10),
        ),
        ActivitySessionData(
            application="Code.exe",
            pid=100,
            window_handle=200,
            window_title="models.py",
            start_time=datetime(2026, 10, 3, 16, 10, tzinfo=UTC),
            end_time=datetime(2026, 10, 3, 16, 30, tzinfo=UTC),
            duration=timedelta(minutes=20),
        ),
    ]

    result = analyze_sessions(sessions)

    assert "sessions" in result
    assert "application_stats" in result

    assert len(result["sessions"]) == 2

    code = result["application_stats"]
    code = code[code["application"] == "Code.exe"].iloc[0]

    assert code["total_duration"] == timedelta(minutes=30)
    assert code["session_count"] == 2
    assert code["avg_session_duration"] == timedelta(minutes=15)

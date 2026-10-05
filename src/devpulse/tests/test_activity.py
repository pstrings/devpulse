import pandas as pd

from devpulse.analytics.activity import (
    add_productivity_metrics,
    calculate_application_stats,
)


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

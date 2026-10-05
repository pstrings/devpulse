import pandas as pd

from devpulse.db.models import ActivitySession

PRODUCTIVE_APPLICATIONS = {
    "Code.exe",
    "vstudio.exe",
    "python.exe",
    "git.exe",
}


def sessions_to_dataframe(sessions: list[ActivitySession]) -> pd.DataFrame:
    """
    Convert a list of ActivitySession objects to a pandas DataFrame.

    Args:
        sessions (list[ActivitySession]): List of ActivitySession objects.

    Returns:
        pd.DataFrame: DataFrame containing the session data.
    """
    records = [
        {
            "application": session.application,
            "pid": session.pid,
            "window_handle": session.window_handle,
            "window_title": session.window_title,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "duration": session.duration,
        }

        for session in sessions
    ]

    return pd.DataFrame(records)


def application_duration_to_dataframe(results) -> pd.DataFrame:
    """
    Convert a list of tuples containing application names and their total durations to a pandas DataFrame.

    Args:
        duration_data (list[tuple[str, int]]): List of tuples where each tuple contains an application name and its total duration.

    Returns:
        pd.DataFrame: DataFrame containing the application names and their total durations.
    """
    return pd.DataFrame(
        results,
        columns=["application", "total_duration"]
    )


def add_usage_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add usage metrics to the DataFrame, including total minutes and percentage of total duration.

    Args:
        df (pd.DataFrame): DataFrame containing application names and their total durations.

    Returns:
        pd.DataFrame: DataFrame with added usage metrics.
    """
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame

    df["total_minutes"] = df["total_duration"] / 60
    df["percentage"] = (df["total_duration"] /
                        df["total_duration"].sum()) * 100
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features to the DataFrame, including hour of the day and day of the week.

    Args:
        df (pd.DataFrame): DataFrame containing session data with start_time and end_time columns.

    Returns:
        pd.DataFrame: DataFrame with added time-based features.
    """
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame

    df["date"] = df["start_time"].dt.date
    df["hour"] = df["start_time"].dt.hour
    df["day_of_week"] = df["start_time"].dt.dayofweek
    df["day_name"] = df["start_time"].dt.day_name()

    return df


def prepare_sessions(sessions):
    df = sessions_to_dataframe(sessions)
    df = add_time_features(df)

    return df


def calculate_application_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate application statistics including total duration, session count, average session duration, and percentage of total duration.

    Args:
        df (pd.DataFrame): DataFrame containing session data with application and duration columns.

    Returns:
        pd.DataFrame: DataFrame containing application statistics.
    """
    application_stats = (
        df.groupby("application")
        .agg(
            total_duration=("duration", "sum"),
            session_count=("application", "size")
        )
        .reset_index()
    )

    application_stats["total_minutes"] = (
        application_stats["total_duration"] / 60)

    application_stats["avg_session_duration"] = (
        application_stats["total_duration"] / application_stats["session_count"])

    application_stats["percentage"] = (
        application_stats["total_duration"] /
        application_stats["total_duration"].sum() * 100)

    return application_stats


def add_productivity_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add productivity metrics to the DataFrame, including a boolean column indicating whether the application is productive.

    Args:
        df (pd.DataFrame): DataFrame containing application statistics.
    """
    df = df.copy()

    df["is_productive"] = df["application"].isin(PRODUCTIVE_APPLICATIONS)

    total_duration = df["duration"].sum()

    productive_duration = df.loc[df["is_productive"], "duration"].sum()

    df["productive_percentage"] = (
        productive_duration / total_duration * 100 if total_duration > 0 else 0
    )

    return df

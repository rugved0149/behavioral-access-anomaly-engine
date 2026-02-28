from datetime import datetime

def extract_time_features(timestamp_str):
    """
    Input: ISO timestamp string
    Output: (hour, day)
    """
    dt = datetime.fromisoformat(timestamp_str)
    return dt.hour, dt.weekday()

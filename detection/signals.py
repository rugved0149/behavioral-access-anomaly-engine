import json
from math import fabs
from baseline.baseline_manager import load_baseline
from db.database import get_connection

def time_deviation_signal(event):
    baseline = load_baseline()

    mean = baseline["mean_access_hour"]
    std = baseline["std_access_hour"]

    if mean is None or std is None:
        return 0.0, "no_time_baseline"

    #  Stability Fix 1: Minimum std floor
    std = max(std, 1.0)

    z_score = abs(event["hour"] - mean) / std

    #  Stability Fix 2: Cap extreme z
    z_score = min(z_score, 6.0)

    #  Stability Fix 3: Smooth non-linear scaling
    # (logistic-like soft curve)
    risk = z_score / (z_score + 3)

    return round(risk, 3), f"time_z={round(z_score,2)}"

def new_device_signal(event):
    baseline = load_baseline()
    known_devices = json.loads(baseline["known_devices"])

    if event["device_fingerprint"] not in known_devices:
        return 0.9, "new_device"

    return 0.0, "known_device"


def new_client_signal(event):
    baseline = load_baseline()
    known_clients = json.loads(baseline["known_clients"])

    if event["client_type"] not in known_clients:
        return 0.6, "new_client"

    return 0.0, "known_client"


def new_network_signal(event):
    baseline = load_baseline()
    known_countries = json.loads(baseline["known_countries"])
    known_asns = json.loads(baseline["known_asns"])

    risk = 0.0
    reasons = []

    if event["country"] not in known_countries:
        risk += 0.4
        reasons.append("new_country")

    if event["asn"] not in known_asns:
        risk += 0.5
        reasons.append("new_asn")

    return min(risk, 1.0), ",".join(reasons) or "known_network"


def burst_signal(event):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM access_events
        WHERE timestamp >= datetime('now', '-1 hour')
    """)

    count = cur.fetchone()[0]
    conn.close()

    baseline = load_baseline()
    threshold = baseline["burst_threshold"]

    if threshold is None:
        return 0.0, "no_burst_baseline"

    if count > threshold:
        return 0.7, f"burst_count={count}"

    return 0.0, "normal_frequency"

def inter_event_gap_signal(event):
    baseline = load_baseline()
    avg_gap = baseline["avg_inter_event_gap"]

    if avg_gap is None or event["time_since_last"] is None:
        return 0.0, "no_gap_baseline"

    current_gap = event["time_since_last"]

    # If 70% smaller than normal → suspicious
    if current_gap < (avg_gap * 0.3):
        return 0.8, f"rapid_gap={round(current_gap,2)}"

    # Mild anomaly
    if current_gap < (avg_gap * 0.6):
        return 0.4, f"fast_gap={round(current_gap,2)}"

    return 0.0, "normal_gap"
import json
from datetime import datetime
from db.database import get_connection
from baseline.stats import update_ema, update_std

# ----------------------------
# Configuration
LEARNING_EVENTS_THRESHOLD = 5
BASELINE_LOCKED = False   # flips automatically after learning

# ----------------------------
# Baseline Access
def load_baseline():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM baseline_profile WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return row


def get_event_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM access_events")
    count = cur.fetchone()[0]
    conn.close()
    return count


def is_learning_mode():
    return get_event_count() < LEARNING_EVENTS_THRESHOLD


# ----------------------------
# Identity Risk Logic
from datetime import datetime
from config import Config

def update_identity_risk(current_risk):
    baseline = load_baseline()

    old_risk = baseline["identity_risk"] or 0.0
    last_updated = baseline["identity_last_updated"]

    from datetime import datetime
    now = datetime.utcnow()

    # Time-aware decay
    if last_updated:
        last_time = datetime.fromisoformat(last_updated)
        hours_passed = (now - last_time).total_seconds() / 3600
        decay_factor = pow(0.95, hours_passed)
        decayed_risk = old_risk * decay_factor
    else:
        decayed_risk = old_risk

    new_risk = min(decayed_risk + current_risk, 1.0)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE baseline_profile
        SET identity_risk = ?,
            identity_last_updated = ?
        WHERE id = 1
    """, (new_risk, now.isoformat()))

    conn.commit()
    conn.close()   
# ----------------------------
# Baseline Learning (ONLY during learning phase)
def update_baseline_with_event(event):
    """
    Baseline is updated ONLY during learning phase.
    After learning, baseline is frozen.
    """

    if not is_learning_mode():
        return  # 🔒 freeze baseline after learning

    baseline = load_baseline()

    # ----------------------------
    # Time modeling (hour behavior)
    # ----------------------------

    mean_hour = update_ema(
        baseline["mean_access_hour"],
        event["hour"]
    )

    std_hour = update_std(
        baseline["std_access_hour"],
        baseline["mean_access_hour"],
        event["hour"]
    )

    # ----------------------------
    # Inter-event gap modeling
    # ----------------------------

    avg_gap = baseline["avg_inter_event_gap"]

    if event["time_since_last"] is not None:
        if avg_gap is None:
            avg_gap = event["time_since_last"]
        else:
            # Exponential moving average (smooth learning)
            avg_gap = (0.8 * avg_gap) + (0.2 * event["time_since_last"])

    # ----------------------------
    # Known sets (identity behavior)
    # ----------------------------

    known_countries = json.loads(baseline["known_countries"])
    known_asns = json.loads(baseline["known_asns"])
    known_clients = json.loads(baseline["known_clients"])
    known_devices = json.loads(baseline["known_devices"])

    if event["country"] not in known_countries:
        known_countries.append(event["country"])

    if event["asn"] not in known_asns:
        known_asns.append(event["asn"])

    if event["client_type"] not in known_clients:
        known_clients.append(event["client_type"])

    if event["device_fingerprint"] not in known_devices:
        known_devices.append(event["device_fingerprint"])

    # ----------------------------
    # Burst threshold learning
    # ----------------------------

    event_count = get_event_count()

    # Conservative baseline for burst
    burst_threshold = max(5, event_count // 2)

    # ----------------------------
    # Save updated baseline
    # ----------------------------

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE baseline_profile SET
            mean_access_hour = ?,
            std_access_hour = ?,
            known_countries = ?,
            known_asns = ?,
            known_clients = ?,
            known_devices = ?,
            burst_threshold = ?,
            avg_inter_event_gap = ?,
            last_updated = ?
        WHERE id = 1
    """, (
        mean_hour,
        std_hour,
        json.dumps(known_countries),
        json.dumps(known_asns),
        json.dumps(known_clients),
        json.dumps(known_devices),
        burst_threshold,
        avg_gap,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
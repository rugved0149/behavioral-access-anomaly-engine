# ingestion/event_ingestor.py

from datetime import datetime
import logging
import json
from detection.classifier import classify_attack
from detection.scorer import compute_risk_score
from detection.decision import make_decision
from db.database import get_connection
from utils.time_utils import extract_time_features
from utils.geoip import lookup_ip
from baseline.baseline_manager import (
    is_learning_mode,
    update_baseline_with_event,
    update_identity_risk
)

REQUIRED_FIELDS = {
    "client_type",
    "access_type",
    "device_fingerprint",
    "fingerprint_data"
}


def validate_event(payload):
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        raise ValueError(f"Missing fields: {missing}")


def get_time_since_last_access():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp FROM access_events ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    last_time = datetime.fromisoformat(row["timestamp"])
    return (datetime.utcnow() - last_time).total_seconds()


def ingest_event(payload):
    validate_event(payload)

    timestamp = payload["timestamp"]
    source_ip = payload["source_ip"]
    client_type = payload["client_type"]
    access_type = payload["access_type"]
    device_fingerprint = payload["device_fingerprint"]
    fingerprint_metadata = json.dumps(payload["fingerprint_data"])

    hour, day = extract_time_features(timestamp)
    country, asn = lookup_ip(source_ip)
    time_since_last = get_time_since_last_access()

    conn = get_connection()
    cur = conn.cursor()

    # ----------------------------
    # Insert event
    # ----------------------------
    cur.execute("""
        INSERT INTO access_events (
            timestamp, hour, day,
            source_ip, country, asn,
            client_type, device_fingerprint,
            fingerprint_metadata,
            access_type, time_since_last
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, hour, day,
        source_ip, country, asn,
        client_type,
        device_fingerprint,
        fingerprint_metadata,
        access_type,
        time_since_last
    ))

    event_id = cur.lastrowid

    cur.execute(
        "SELECT * FROM access_events WHERE id = ?",
        (event_id,)
    )
    event_row = cur.fetchone()

    conn.commit()
    conn.close()

    logging.info(
        f"Event ingested | id={event_id} ip={source_ip} client={client_type}"
    )

    # ----------------------------
    # Detection Phase
    # ----------------------------

    if is_learning_mode():
        verdict = "LEARNING"
        risk_score = 0.0
        attack_type = "BASELINE_BUILDING"
        reasons = ["learning_phase"]
        explainability = None
        update_baseline_with_event(event_row)

    else:
        risk_score, signal_details, synergy_multiplier = compute_risk_score(event_row)
        verdict = make_decision(risk_score)
        attack_type = classify_attack(signal_details)
        reasons = [s["reason"] for s in signal_details]

        explainability = json.dumps({
            "signals": signal_details,
            "synergy_multiplier": synergy_multiplier,
            "final_score": risk_score
        })

    # Update rolling identity risk
    update_identity_risk(risk_score)

    # ----------------------------
    # Store decision
    # ----------------------------
    # ----------------------------
# Store decision
# ----------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO risk_decisions (
            event_id, risk_score, verdict, attack_type,
            reasons, explainability, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        event_id,
        risk_score,
        verdict,
        attack_type,
        ",".join(reasons),
        explainability
    ))

    conn.commit()
    conn.close()

    return event_id
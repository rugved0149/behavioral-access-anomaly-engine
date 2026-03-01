import os
from functools import wraps
from config import Config
from flask import request
import hashlib
from ingestion.event_ingestor import ingest_event
from flask import Flask, jsonify
import logging
from datetime import datetime
from flask import render_template
from db.database import get_connection
from utils.fingerprint import generate_device_fingerprint

# ----------------------------
# App Configuration
# ----------------------------
app = Flask(__name__)

# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logging.info("Application starting...")

def require_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or \
           auth.username != Config.AUTH_USERNAME or \
           auth.password != Config.AUTH_PASSWORD:
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated

# ----------------------------
# Health Check Endpoint
# ----------------------------
@app.route("/health", methods=["GET"])
def health_check():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return jsonify({
            "status": "ok",
            "time": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route("/", methods=["GET"])
def dashboard():
    import json

    conn = get_connection()
    cur = conn.cursor()

    # --- Metrics ---
    cur.execute("SELECT COUNT(*) FROM access_events")
    total_events = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM risk_decisions WHERE verdict='SUSPICIOUS'")
    suspicious = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM risk_decisions WHERE verdict='HIGH_RISK'")
    high_risk = cur.fetchone()[0]

    # --- Identity Risk ---
    cur.execute("SELECT identity_risk FROM baseline_profile WHERE id=1")
    row = cur.fetchone()
    identity_risk = row[0] if row and row[0] else 0.0

    # Cap safety (should already be capped, but defensive programming)
    identity_risk = min(identity_risk, 1.0)

    # Risk meter percentage (0–100)
    identity_risk_percent = round(identity_risk * 100)

    # --- Recent Decisions ---
    cur.execute("""
        SELECT event_id, risk_score, verdict,
               attack_type, reasons, explainability
        FROM risk_decisions
        ORDER BY id DESC
        LIMIT 15
    """)
    rows = cur.fetchall()

    recent = []
    for r in rows:
        r = dict(r)

        # Parse explainability JSON safely
        if r["explainability"]:
            r["explainability"] = json.loads(r["explainability"])
        else:
            r["explainability"] = None

        recent.append(r)

    conn.close()

    return render_template(
        "dashboard.html",
        total_events=total_events,
        suspicious=suspicious,
        high_risk=high_risk,
        identity_risk=identity_risk,
        identity_risk_percent=identity_risk_percent,
        recent=recent
    )

@app.route("/api/dashboard")
def dashboard_api():
    import json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM access_events")
    total_events = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM risk_decisions WHERE verdict='SUSPICIOUS'")
    suspicious = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM risk_decisions WHERE verdict='HIGH_RISK'")
    high_risk = cur.fetchone()[0]

    cur.execute("SELECT identity_risk FROM baseline_profile WHERE id=1")
    row = cur.fetchone()
    identity_risk = row[0] if row and row[0] else 0.0

    cur.execute("""
        SELECT event_id, risk_score, verdict,
               attack_type
        FROM risk_decisions
        ORDER BY id DESC
        LIMIT 10
    """)
    events = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify({
        "total_events": total_events,
        "suspicious": suspicious,
        "high_risk": high_risk,
        "identity_risk": identity_risk,
        "events": events
    })
@app.route("/test")
def test():
    return "test ok"

@app.route("/event", methods=["POST"])
@require_basic_auth
def ingest_access_event():

    try:
        payload = request.get_json(silent=True) or {}

        payload["timestamp"] = datetime.utcnow().isoformat()

        real_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        payload["source_ip"] = real_ip

        user_agent = request.headers.get("User-Agent", "unknown")

        fingerprint, fingerprint_data = generate_device_fingerprint(
            user_agent,
            payload.get("client_type", "")
        )

        payload["device_fingerprint"] = fingerprint
        payload["fingerprint_data"] = fingerprint_data

        event_id = ingest_event(payload)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT risk_score, verdict, reasons
            FROM risk_decisions
            WHERE event_id = ?
        """, (event_id,))
        decision = cur.fetchone()
        conn.close()

        # ✅ SAFETY CHECK ADDED HERE
        if decision is None:
            return jsonify({
                "status": "error",
                "error": "Decision not generated"
            }), 500

        return jsonify({
            "status": "accepted",
            "event_id": event_id,
            "risk_score": decision["risk_score"],
            "verdict": decision["verdict"],
            "reasons": decision["reasons"].split(",") if decision["reasons"] else []
        }), 201

    except ValueError as ve:
        logging.warning(f"Invalid event: {ve}")
        return jsonify({
            "status": "error",
            "error": str(ve)
        }), 400

    except Exception as e:
        print("DEBUG ERROR:", e)  # Temporary debug
        return jsonify({
            "status": "error",
            "error": "internal server error"
        }), 500
# Application Entry
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
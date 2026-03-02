# 🛡 Behavioral Access Anomaly & Identity Risk Engine

A multi-signal behavioral security engine that detects anomalous access patterns using contextual signal correlation, weighted risk scoring, synergy amplification, and identity-level risk memory.

Unlike static rule-based systems, this engine models behavioral context dynamically and provides explainable risk decisions.

---

# 🚀 Project Objective

Traditional security tools detect threats in isolation:

* Suspicious IP
* New device
* Burst of requests
* Unusual login time

Real attacks are multi-dimensional.

This project was built to:

* Correlate multiple weak signals
* Apply weighted risk scoring
* Amplify risk under multi-signal synergy
* Maintain rolling identity-level memory
* Provide structured explainability
* Classify behavioral attack types

---

# 🧠 Core Design Principles

1. Context over single events
2. Weighted multi-signal scoring
3. Synergy amplification
4. Identity risk persistence
5. Explainability-first detection

---

# 🏗 System Architecture

```
Client Request
      ↓
Basic Auth
      ↓
Device Fingerprint
      ↓
Event Ingestion
      ↓
Signal Extraction
      ↓
Weighted Scoring
      ↓
Synergy Amplifier
      ↓
Decision Engine
      ↓
Identity Risk Update
      ↓
Dashboard / API
```

---

# 🔍 Behavioral Signals Modeled

### 1️⃣ Time Deviation

* Z-score based deviation from learned mean access hour
* Detects unusual access timing

### 2️⃣ Network Familiarity

* Checks known country / ASN
* New geographic origin increases risk

### 3️⃣ Device Fingerprint

Generated using SHA-256 from:

* Browser
* OS
* Device class
* Client type
* Headers

New device → high risk

### 4️⃣ Client Type Shift

Detects change:

* browser → script
* read → write

### 5️⃣ Burst Detection

Detects rapid spikes in event frequency.

Example:

```
burst_count=20
```

### 6️⃣ Inter-Event Gap

Detects automation-like rapid timing.

```
rapid_gap=0.06
```

---

# ⚖ Weighted Risk Model

Each signal contributes:

```
contribution = raw_risk × weight
```

If 3+ signals trigger:

```
total_score × 1.25
```

Scores are capped at **1.0**.

### Verdict Classification

| Score Range | Verdict    |
| ----------- | ---------- |
| 0.00–0.39   | NORMAL     |
| 0.40–0.69   | SUSPICIOUS |
| 0.70–1.00   | HIGH_RISK  |

---

# 🧬 Identity Risk Memory

The engine maintains a rolling:

```
identity_risk
```

* Aggregates risk across events
* Gradually decays
* Saturates at 1.0 under sustained anomaly

This models long-term compromise behavior.

---

# 🧾 Explainability

Each decision stores structured JSON:

```json
{
  "signals": [
    {
      "name": "burst",
      "raw_risk": 0.7,
      "weight": 0.3,
      "contribution": 0.21,
      "reason": "burst_count=20"
    }
  ],
  "synergy_multiplier": 1.25,
  "final_score": 1.0
}
```

This ensures transparency and auditability.

---

# 🌐 API Documentation

## 🔹 POST /event

**Authentication:** Basic Auth

Default demo credentials:

```
Username: admin
Password: admin123
```

### Headers

```
Content-Type: application/json
User-Agent: <any string>
```

### Body

```json
{
  "client_type": "browser | script | automation",
  "access_type": "read | write"
}
```

### Example Response

```json
{
  "status": "accepted",
  "event_id": 15,
  "risk_score": 1.0,
  "verdict": "HIGH_RISK",
  "reasons": [
    "new_device",
    "new_client",
    "burst_count=20"
  ]
}
```

---

# 📊 Dashboard

Accessible at:

```
https://behavioral-access-anomaly-engine.onrender.com/
```

Displays:

* Identity Risk Meter
* Event counters
* Suspicious / High-risk counts
* Attack type classification
* Signal breakdown per event

Auto-refresh every 5 seconds.

---

# 🧪 Reviewer Demonstration Guide

### Step 1 — Open Dashboard

Visit the live URL.

### Step 2 — Generate Normal Behavior

Send:

```json
{
  "client_type": "browser",
  "access_type": "read"
}
```

3–4 times → NORMAL verdict.

### Step 3 — Simulate Burst Attack

Send rapid repeated:

```json
{
  "client_type": "script",
  "access_type": "read"
}
```

→ burst_count increases
→ rapid_gap triggered
→ HIGH_RISK

### Step 4 — Trigger Multi-Signal Synergy

Use:

```json
{
  "client_type": "automation",
  "access_type": "write"
}
```

Rapid repetition → synergy multiplier applied → score capped at 1.0.

---

# 🚀 Deployment (Render)

## Build Command

```
pip install -r requirements.txt
```

## Start Command

```
gunicorn app:app
```

## Environment Variables (Optional)

```
AUTH_USERNAME=admin
AUTH_PASSWORD=admin123
```

SQLite auto-initializes on startup.

---

# 📦 Technology Stack

* Python 3.11
* Flask
* SQLite
* Gunicorn
* user-agents
* SHA-256 fingerprinting
* Render deployment

---

# ⚠ Limitations

* SQLite (demo-grade storage)
* No distributed scaling
* No real GeoIP database
* No rate limiting
* Not horizontally scalable

---

# 🔭 Future Enhancements

* PostgreSQL backend
* Redis burst tracking
* JWT authentication
* GeoIP integration
* ML-based anomaly scoring
* Rate limiting
* Alert webhooks

---

# 🏁 Summary

This project demonstrates a contextual behavioral risk engine using:

* Multi-signal correlation
* Weighted scoring
* Synergy amplification
* Identity-level memory
* Structured explainability

--- 

# 👤 Author

Rugved Suryawanshi
Computer Science (Software) Engineering Student

---

## License

This project is licensed under the **MIT License**.

The MIT License permits use, modification, distribution, and private deployment of this software with proper attribution.

See the `LICENSE` file in this repository for full legal text.
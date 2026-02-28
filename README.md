# 🛡 Behavioral Access Anomaly & Identity Risk Engine

A multi-signal behavioral security engine that detects anomalous access patterns using contextual signal correlation, weighted risk scoring, synergy amplification, and identity-level memory modeling.

This system does **not rely on static signatures**.
Instead, it models user behavior dynamically and detects deviations in real time.

---

# 🚀 Project Objective

Most traditional security mechanisms detect threats in isolation:

* A suspicious IP
* A new device
* A burst of requests
* A login at an unusual time

However, real attacks are multi-dimensional.

This project was designed to:

* Correlate multiple weak signals
* Assign weighted risk contributions
* Amplify risk when multiple signals co-occur
* Maintain rolling identity-level risk memory
* Provide explainable AI-style breakdown of risk decisions
* Classify behavioral attack patterns

---

# 🧠 Core Design Philosophy

The engine follows five core principles:

1. **Context over single events**
2. **Weighted multi-signal scoring**
3. **Synergy amplification**
4. **Identity memory persistence**
5. **Explainability-first detection**

---

# 🏗 System Architecture

```
Client Request
      ↓
Basic Auth Layer
      ↓
Fingerprint Generator
      ↓
Event Ingestion Engine
      ↓
Signal Extraction Layer
      ↓
Weighted Risk Scoring
      ↓
Synergy Amplifier
      ↓
Decision Engine
      ↓
Identity Risk Update
      ↓
Explainability Storage
      ↓
Dashboard / API Output
```

---

# 🔍 Behavioral Signals Modeled

The system currently models six contextual signals:

---

## 1️⃣ Time Deviation Signal

Detects deviation from baseline mean access hour.

* Uses Z-score normalization
* Learns mean and standard deviation during learning phase
* Detects unusual time-of-access

Example:

```
time_z=6.0
```

---

## 2️⃣ Network Familiarity Signal

Checks if country / ASN has been seen before.

* New geographic origin increases risk
* Known network contributes 0 risk

---

## 3️⃣ Device Fingerprint Signal

Uses SHA-256 fingerprint generated from:

* Browser
* Browser version
* OS
* OS version
* Device class
* Client type
* Language headers

New device → high raw risk

---

## 4️⃣ Client Type Shift Signal

Detects shift in access mode:

Examples:

* browser → script
* browser → automation
* read → write

---

## 5️⃣ Burst Detection Signal

Detects high-frequency event spikes.

Example:

```
burst_count=20
```

Captures:

* Credential stuffing
* API abuse
* Brute force bursts

---

## 6️⃣ Inter-Event Gap Signal

Measures time difference between consecutive events.

Triggers when:

* Very short gap
* Suspicious automation-like timing

Example:

```
rapid_gap=0.06
```

---

# ⚖ Weighted Risk Model

Each signal contributes:

```
contribution = raw_risk × weight
```

Example weights:

| Signal  | Weight |
| ------- | ------ |
| Time    | 0.20   |
| Network | 0.25   |
| Device  | 0.35   |
| Client  | 0.30   |
| Burst   | 0.30   |
| Gap     | 0.30   |

Total risk is aggregated.

---

# 🔥 Synergy Amplification

If 3 or more signals trigger:

```
total_score × 1.25
```

This models real-world coordinated behavior patterns.

Example from test run:

```json
"synergy_multiplier": 1.25,
"final_score": 1.0
```

---

# 🎯 Verdict Classification

Risk Score Range → Verdict:

| Score       | Verdict    |
| ----------- | ---------- |
| 0.00 – 0.39 | NORMAL     |
| 0.40 – 0.69 | SUSPICIOUS |
| 0.70 – 1.00 | HIGH_RISK  |

Scores are capped at 1.0.

---

# 🧬 Identity-Level Risk Memory

The engine maintains:

```
identity_risk
```

This is a rolling risk memory updated after each event.

Characteristics:

* Capped at 1.0
* Decay factor applied over time
* Represents cumulative behavioral drift

This models long-term compromise patterns.

---

# 🧾 Explainability Engine

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

This allows:

* Transparency
* Debugging
* Review validation
* Model trust

---

# 📊 Dashboard Features

The web dashboard displays:

* Total events
* Suspicious count
* High-risk count
* Identity risk meter
* Attack type classification
* Signal breakdown per event

Auto-refresh every 5 seconds.

---

# 🔐 Authentication

API endpoint requires HTTP Basic Authentication.

Credentials (default demo):

```
Username: admin
Password: admin123
```

---

# 🌐 API Documentation

## POST /event

### Authentication

Basic Auth required.

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

---

## Response Example

```json
{
  "status": "accepted",
  "event_id": 15,
  "risk_score": 1.0,
  "verdict": "HIGH_RISK",
  "reasons": [
    "time_z=6.0",
    "new_device",
    "new_client",
    "burst_count=20",
    "rapid_gap=0.06"
  ]
}
```

---

# 🧪 Testing Scenarios

The engine was validated against:

* Learning phase modeling
* Burst escalation
* Rapid inter-event gap
* Device shift
* Client type shift
* Time deviation anomaly
* Multi-signal synergy activation
* Identity risk saturation

Explainability JSON verified for correctness.

---

# 📦 Technology Stack

* Python 3.11
* Flask
* SQLite
* user-agents parser
* Gunicorn (production)
* SHA-256 fingerprinting
* Render deployment

---

# 🧠 Why This Is Not a Basic Project

This is not just:

* A rule-based detector
* A simple threshold system
* A static anomaly flagger

It implements:

* Statistical deviation modeling
* Context-aware multi-signal correlation
* Weighted risk mathematics
* Synergy amplification logic
* Identity persistence modeling
* Explainable scoring
* API + UI separation
* Authentication layer

---

# 📈 Real-World Use Cases

* API abuse detection
* Account takeover detection
* Insider behavioral monitoring
* Session anomaly modeling
* Fraud scoring prototype
* Zero-trust adaptive authentication model

---

# ⚠ Known Limitations

* SQLite used for demo purposes
* No distributed storage
* No real IP geo database in demo mode
* Not optimized for horizontal scaling

Good. Now we complete this properly.

Below is **Part 2** of your README — reviewer-focused, deployment-ready, and strategically framed.

You can append this directly below Part 1.

---

# 🧪 Reviewer Demonstration Guide

This section explains how the system should be evaluated.

---

## 🔹 Step 1 — Open Dashboard

Visit:

```
https://<your-app-name>.onrender.com/
```

You will see:

* Identity Risk Meter
* Total Events Counter
* Suspicious Count
* High-Risk Count
* Recent Decision Cards
* Signal Breakdown per Event

Initially, metrics may be low or zero.

---

## 🔹 Step 2 — Generate Normal Behavior

Using Postman or curl:

```
POST /event
```

Basic Auth:

```
Username: admin
Password: admin123
```

Body:

```json
{
  "client_type": "browser",
  "access_type": "read"
}
```

Send 3–4 times.

Expected:

* LEARNING phase initially
* Then NORMAL verdict
* Risk score close to 0.0

---

## 🔹 Step 3 — Simulate Burst Behavior

Send rapid repeated requests with:

```json
{
  "client_type": "script",
  "access_type": "read"
}
```

Use a different User-Agent.

Expected:

* burst_count increases
* rapid_gap triggered
* Verdict escalates to HIGH_RISK
* Identity risk meter increases

---

## 🔹 Step 4 — Trigger Multi-Signal Synergy

Use:

```json
{
  "client_type": "automation",
  "access_type": "write"
}
```

Combined with rapid requests.

Expected:

* new_device
* new_client
* burst
* gap
* time deviation
* synergy_multiplier = 1.25
* final_score capped at 1.0

---

## 🔹 Step 5 — Observe Explainability

Click “View Signal Breakdown” in dashboard.

You should see:

* Raw risk per signal
* Weight per signal
* Contribution
* Synergy multiplier
* Final computed score

This demonstrates model transparency.

---

# 📂 Project Structure

```
behavioral_access_anomaly/
│
├── app.py
├── config.py
├── requirements.txt
│
├── ingestion/
│   └── event_ingestor.py
│
├── detection/
│   ├── scorer.py
│   ├── signals.py
│   └── decision.py
│
├── baseline/
│   └── baseline_manager.py
│
├── utils/
│   ├── fingerprint.py
│   ├── geoip.py
│   └── time_utils.py
│
├── db/
│   ├── database.py
│   ├── schema.sql
│   └── init_db.py
│
├── templates/
│   └── dashboard.html
│
└── access_behavior.db
```

---

# 🚀 Deployment Instructions (Render)

---

## 1️⃣ Ensure requirements.txt exists

Generate:

```
pip freeze > requirements.txt
```

Ensure it contains:

* Flask
* gunicorn
* user-agents
* any other dependencies

---

## 2️⃣ Start Command

Set start command in Render:

```
gunicorn app:app
```

---

## 3️⃣ Build Command

```
pip install -r requirements.txt
```

---

## 4️⃣ Optional Production Hardening

Move credentials into environment variables:

```
AUTH_USERNAME=admin
AUTH_PASSWORD=admin123
```

And modify config.py accordingly.

---

# 🔐 Security Considerations

* Basic authentication protects ingestion endpoint
* Device fingerprint uses SHA-256 hashing
* Risk scores capped to prevent overflow
* Explainability stored as structured JSON
* Defensive checks added for missing decision rows

For production:

* Replace SQLite with PostgreSQL
* Add rate limiting
* Add JWT authentication
* Add TLS enforcement
* Add IP reputation integration

---

# 🧬 Attack Classification Logic

The engine classifies attack patterns:

Examples:

* BURST_ABUSE
* DEVICE_SHIFT
* CLIENT_SHIFT
* TIME_ANOMALY
* MULTI_SIGNAL_ANOMALY

Classification is based on dominant triggering signals.

---

# 📈 Identity Risk Modeling

Identity risk:

* Aggregates risk across events
* Decays gradually over time
* Represents long-term behavioral drift
* Saturates at 1.0 under sustained anomaly

This models persistent compromise scenarios.

---

# 🔭 Future Improvements

Planned enhancements:

* PostgreSQL backend
* Redis for burst window tracking
* ML-based anomaly scoring
* GeoIP database integration
* Real IP reputation scoring
* JWT authentication
* Role-based access control
* Admin dashboard analytics
* API rate limiting
* Alert webhook integration

---

# 📊 Research & Engineering Value

This project demonstrates:

* Behavioral modeling principles
* Statistical anomaly detection
* Risk-based scoring architecture
* Multi-signal correlation
* Explainable AI concepts
* Security engineering design
* API design + UI integration
* Production deployment awareness

---

# 🏁 Final Statement

This project demonstrates how behavioral signals, when correlated and weighted intelligently, can provide a far more accurate and explainable risk assessment than isolated security rules.

It is intended as a prototype behavioral risk engine and conceptual foundation for adaptive security systems and zero-trust environments.

---

## 14. Author

Rugved Suryawanshi
Computer Science (Software) Engineering Student

---

## 15. License

This project is licensed under the **MIT License**.

The MIT License permits use, modification, distribution, and private deployment of this software with proper attribution.

See the `LICENSE` file in this repository for full legal text.

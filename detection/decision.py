from baseline.baseline_manager import load_baseline


def make_decision(risk_score):
    baseline = load_baseline()
    identity_risk = baseline["identity_risk"] or 0.0

    # Escalate based on accumulated risk
    combined = min(risk_score + (identity_risk * 0.5), 1.0)

    if combined < 0.30:
        return "NORMAL"
    elif combined < 0.60:
        return "SUSPICIOUS"
    else:
        return "HIGH_RISK"
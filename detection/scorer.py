from detection.signals import (
    time_deviation_signal,
    new_network_signal,
    burst_signal,
    new_device_signal,
    new_client_signal,
    inter_event_gap_signal
)

def compute_risk_score(event):
    signals = []

    def add_signal(name, raw_risk, weight, reason):
        contribution = raw_risk * weight
        signals.append({
            "name": name,
            "raw_risk": round(raw_risk, 3),
            "weight": weight,
            "contribution": round(contribution, 3),
            "reason": reason
        })
        return contribution

    triggered = 0
    total = 0.0

    # Time
    r, reason = time_deviation_signal(event)
    if r > 0: triggered += 1
    total += add_signal("time", r, 0.20, reason)

    # Network
    r, reason = new_network_signal(event)
    if r > 0: triggered += 1
    total += add_signal("network", r, 0.25, reason)

    # Device
    r, reason = new_device_signal(event)
    if r > 0: triggered += 1
    total += add_signal("device", r, 0.35, reason)

    # Client
    r, reason = new_client_signal(event)
    if r > 0: triggered += 1
    total += add_signal("client", r, 0.30, reason)

    # Burst
    r, reason = burst_signal(event)
    if r > 0: triggered += 1
    total += add_signal("burst", r, 0.30, reason)

    # Gap
    r, reason = inter_event_gap_signal(event)
    if r > 0: triggered += 1
    total += add_signal("gap", r, 0.30, reason)

    synergy_multiplier = 1.0
    if triggered >= 3:
        synergy_multiplier = 1.25
        total *= synergy_multiplier

    final_score = min(total, 1.0)

    return final_score, signals, synergy_multiplier
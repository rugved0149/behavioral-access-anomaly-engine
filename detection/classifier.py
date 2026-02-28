# detection/classifier.py

def classify_attack(signal_details):
    triggered = [s for s in signal_details if s["raw_risk"] > 0]

    names = [s["name"] for s in triggered]

    if len(triggered) >= 3:
        return "MULTI_VECTOR_ATTACK"

    if "gap" in names and "burst" in names:
        return "AUTOMATION"

    if "device" in names and "network" in names:
        return "DEVICE_COMPROMISE"

    if "device" in names:
        return "DEVICE_ANOMALY"

    if "network" in names:
        return "NETWORK_ANOMALY"

    if "time" in names:
        return "TIME_ANOMALY"

    if "burst" in names:
        return "BURST_ABUSE"

    return "NORMAL_BEHAVIOR"
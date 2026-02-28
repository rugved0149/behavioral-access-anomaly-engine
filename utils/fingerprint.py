import hashlib
import json
from user_agents import parse


def generate_device_fingerprint(user_agent_string, client_type):

    ua = parse(user_agent_string)

    fingerprint_data = {
        "browser": ua.browser.family,
        "browser_version": ua.browser.version_string,
        "os": ua.os.family,
        "os_version": ua.os.version_string,
        "device_class": (
            "mobile" if ua.is_mobile else
            "tablet" if ua.is_tablet else
            "pc" if ua.is_pc else
            "bot" if ua.is_bot else
            "unknown"
        ),
        "client_type": client_type
    }

    fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)

    fingerprint_hash = hashlib.sha256(
        fingerprint_json.encode()
    ).hexdigest()

    return fingerprint_hash, fingerprint_data
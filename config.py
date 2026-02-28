import os


class Config:

    # API Key (Optional)
    API_KEY = os.environ.get("API_KEY", "dev-secret-key")

    # Basic Auth Credentials
    AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "admin")
    AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "admin123")

    # Risk Behavior
    IDENTITY_DECAY = 0.95
    MAX_IDENTITY_RISK = 1.0
    SYNERGY_MULTIPLIER = 1.25

    NORMAL_THRESHOLD = 0.30
    SUSPICIOUS_THRESHOLD = 0.60

    TIME_WEIGHT = 0.20
    NETWORK_WEIGHT = 0.25
    DEVICE_WEIGHT = 0.35
    CLIENT_WEIGHT = 0.30
    BURST_WEIGHT = 0.20
    GAP_WEIGHT = 0.30
import requests
from datetime import datetime, timedelta

URL = "http://127.0.0.1:5000/event"

def send_event(ts, ip, client="browser", access="read"):
    payload = {
        "timestamp": ts.isoformat(),
        "source_ip": ip,
        "client_type": client,
        "access_type": access
    }
    r = requests.post(URL, json=payload)
    print(r.json())


# Normal behavior
base_time = datetime.utcnow().replace(hour=10, minute=0)

for i in range(10):
    send_event(base_time + timedelta(minutes=i), "192.168.1.10")

# Time anomaly
send_event(base_time.replace(hour=3), "192.168.1.10")

# Network anomaly
send_event(base_time, "8.8.8.8")

# Burst anomaly
for i in range(30):
    send_event(datetime.utcnow(), "192.168.1.10", client="script")

def lookup_ip(ip_address):
    """
    MOCK geo lookup.
    Replace later if needed.
    """
    if ip_address.startswith("192.168"):
        return "IN", "AS_LOCAL"
    elif ip_address.startswith("10."):
        return "IN", "AS_PRIVATE"
    elif ip_address.startswith("8.8"):
        return "US", "AS_GOOGLE"
    else:
        return "UNKNOWN", "AS_UNKNOWN"

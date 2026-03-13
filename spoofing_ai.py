def calculate_spoofing_score(user_data, collected_data):
    score = 0

    # 1. VPN / Proxy detection
    if collected_data.get("ip_type") in ["vpn", "proxy", "datacenter"]:
        score += 40

    # 2. Timezone mismatch
    if user_data["default_timezone"] != collected_data.get("timezone"):
        score += 20

    # 3. Distance check (GPS)
    from geopy.distance import geodesic
    user_coords = (user_data["default_lat"], user_data["default_lng"])
    collected_coords = (collected_data.get("lat"), collected_data.get("lng"))
    distance_km = geodesic(user_coords, collected_coords).km
    if distance_km > 100:  # مسافة أكبر من 100 كم → زيادة Score
        score += 20

    # 4. Fingerprint mismatch placeholder
    if collected_data.get("device_id") != user_data.get("device_id"):
        score += 20

    return min(score, 100)

def verdict_from_score(score):
    if score >= 50:
        return "SPOOFED"
    return "NOT SPOOFED"

from geopy.distance import geodesic

def calculate_distance(gps_lat, gps_lng, ip_lat, ip_lng):

    gps = (gps_lat, gps_lng)
    ip = (ip_lat, ip_lng)

    distance = geodesic(gps, ip).km

    return distance

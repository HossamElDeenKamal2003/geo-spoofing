import requests

def get_ip_info(ip):

    url = f"http://ip-api.com/json/{ip}"

    data = requests.get(url).json()

    return {
        "country": data.get("country"),
        "isp": data.get("isp"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "timezone": data.get("timezone")
    }

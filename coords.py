import requests
import time

barangays = [
    "Bagbaguin Santa Maria Bulacan",
    "Balasing Santa Maria Bulacan",
    "Buenavista Santa Maria Bulacan",
    "Bulac Santa Maria Bulacan",
    "Camangyanan Santa Maria Bulacan",
    "Cay Pombo Santa Maria Bulacan",
    "Caysio Santa Maria Bulacan",
    "Catmon Santa Maria Bulacan",
    "Guyong Santa Maria Bulacan",
    "Lalakhan Santa Maria Bulacan",
    "Mag-asawang Sapa Santa Maria Bulacan",
    "Mahabang Parang Santa Maria Bulacan",
    "Manggahan Santa Maria Bulacan",
    "Parada Santa Maria Bulacan",
    "Poblacion Santa Maria Bulacan",
    "Pulong Buhangin Santa Maria Bulacan",
    "San Gabriel Santa Maria Bulacan",
    "San Jose Patag Santa Maria Bulacan",
    "San Vicente Santa Maria Bulacan",
    "Santa Clara Santa Maria Bulacan",
    "Santa Cruz Santa Maria Bulacan",
    "Silangan Santa Maria Bulacan",
    "Tabing Ilog Santa Maria Bulacan",
    "Tumana Santa Maria Bulacan",
]

def get_coordinates(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json",
        "limit": 1,
        "countrycodes": "ph"
    }
    headers = {
        "User-Agent": "StaMariaTrafficApp/1.0 (contact: bufddoge@gmail.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return (lat, lon)
        else:
            return ("Not found", "Not found")
    except Exception as e:
        return ("Error", str(e))

print("Fetching coordinates for Sta. Maria barangays...\n")
barangay_coords = {}
for b in barangays:
    lat, lon = get_coordinates(b)
    barangay_coords[b] = (lat, lon)
    print(f"{b}: {lat}, {lon}")
    time.sleep(2)  # polite delay

print("\nFinal dictionary of barangay coordinates:")
print(barangay_coords)


import requests
from datetime import datetime

# ==========================
# CONFIG
# ==========================
API_KEY = "CpIfmNNZcNZ81lmm9znSzdaaeVTAKLaI"
BBOX = "120.9756353,14.83544,120.9776353,14.83744"


URL = "https://api.tomtom.com/traffic/services/5/incidentDetails"  # ✅ correct version

# ==========================
# MAPPINGS
# ==========================
ICON_CATEGORY_MAP = {
    0: "❓ Unknown",
    1: "🚓 Accident",
    2: "🌫 Fog",
    3: "⚠️ Dangerous Conditions",
    4: "🌧 Rain",
    5: "❄️ Ice",
    6: "🚦 Traffic Jam",
    7: "⛔ Lane Closed",
    8: "🚧 Road Closed",
    9: "👷 Road Works",
    10: "💨 Wind",
    11: "🌊 Flooding",
    14: "🔧 Broken Down Vehicle"
}

MAGNITUDE_MAP = {
    0: "❓ Unknown",
    1: "🟢 Minor",
    2: "🟡 Moderate",
    3: "🔴 Major",
    4: "⚪ Undefined"
}

# ==========================
# REQUEST FIELDS
# ==========================
FIELDS = (
    "{incidents{"
    "type,"
    "properties{"
    "id,iconCategory,magnitudeOfDelay,startTime,endTime,"
    "from,to,length,delay,roadNumbers,timeValidity,"
    "probabilityOfOccurrence,events{code,description,iconCategory}"
    "},"
    "geometry{type,coordinates}"
    "}}"
)

params = {
    "key": API_KEY,
    "bbox": BBOX,
    "fields": FIELDS,
    "language": "en-GB",
    "timeValidityFilter": "present"
}

# ==========================
# API CALL
# ==========================
response = requests.get(URL, params=params)

if response.status_code != 200:
    print("❌ API ERROR:", response.status_code)
    print(response.text)
    exit()

data = response.json()
incidents = data.get("incidents", [])

print(f"\n🚦 TOTAL INCIDENTS FOUND: {len(incidents)}\n")

# ==========================
# FORMATTED PRINT
# ==========================
def format_time(ts):
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt.strftime("%m/%d/%y %I:%M %p")  # ✅ 12-hour format with AM/PM
        except Exception:
            return ts
    return "N/A"



for i, incident in enumerate(incidents, start=1):
    props = incident["properties"]

    # Format length (meters) to 2 decimal places
    length_m = props.get("length")
    length_fmt = f"{length_m:.2f} m" if length_m is not None else "N/A"

    # Convert delay (seconds) to minutes:seconds format
    delay_s = props.get("delay")
    if delay_s is not None:
        minutes = delay_s // 60
        seconds = delay_s % 60
        delay_fmt = f"{minutes:02d}:{seconds:02d} (mm:ss)"
    else:
        delay_fmt = "N/A"

    # Format start and end times
    start_fmt = format_time(props.get("startTime"))
    end_fmt = format_time(props.get("endTime"))

    # ==========================
    # BEAUTIFUL OUTPUT
    # ==========================
  
    print(f"🛑 Type              : {ICON_CATEGORY_MAP.get(props.get('iconCategory'))}")
    print(f"📊 Delay Severity    : {MAGNITUDE_MAP.get(props.get('magnitudeOfDelay'))}")
    print(f"⏳ Status            : {props.get('timeValidity')}")
    print(f"🕒 Start Time        : {start_fmt}")
    print(f"🕒 End Time          : {end_fmt}")
    print(f"➡️ From              : {props.get('from')}")
    print(f"➡️ To                : {props.get('to')}")
    print(f"📏 Length            : {length_fmt}")
    print(f"⏱ Delay             : {delay_fmt}")
    print(f"🎲 Probability       : {props.get('probabilityOfOccurrence')}")

    print("\n📌 Events:")
    for event in props.get("events", []):
        print(f"   • {props.get('description')}")

    print("═" * 70 + "\n")

print("✅ Done.")

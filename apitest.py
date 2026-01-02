
import os
import requests

API_KEY = os.getenv("TOMTOM_API_KEY", "CpIfmNNZcNZ81lmm9znSzdaaeVTAKLaI")

# --- Traffic Flow endpoint ---
FLOW_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
flow_params = {
    "point": "14.7996,120.9317",  # Bocaue example
    "key": API_KEY
}

# --- Traffic Incidents endpoint ---
INCIDENTS_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails"
Main_params = {
    "bbox": "120.90,14.65,121.10,14.90",  # Metro Manila/Bulacan bounding box
    "key": API_KEY
}

def get_data(url, params):
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error:", resp.status_code, resp.text)
        return {}

def main():
    # Call Flow API
    flow_data = get_data(FLOW_URL, flow_params)
    flow = flow_data.get("flowSegmentData", {})
    print("Traffic Flow Segment Data:")
    print("Current speed (km/h):", flow.get("currentSpeed"))
    print("Free flow speed (km/h):", flow.get("freeFlowSpeed"))
    print("Confidence:", flow.get("confidence"))
    Road_Close = flow.get("roadClosure")
    if Road_Close == True :
        print("RoadClosure: There is ROAD CLOSURE!") 
    else:
        print("RoadClosure: There is no ROAD CLOSURE!")
    

    # Call Incidents API
    incidents_data = get_data(INCIDENTS_URL, incidents_params)
    incidents = incidents_data.get("incidents", []) or incidents_data.get("features", [])
    print("\nTraffic Incidents:")
    for inc in incidents[:3]:  # show first 3 incidents
        props = inc.get("properties", {})
        print("-", props.get("description"), "| Severity:", props.get("magnitudeOfDelay"))

if __name__ == "__main__":
    main()

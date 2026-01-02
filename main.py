import json
import openrouteservice
import os
import requests
# client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdiYzQxMTY2NzVmZDQ2Mzc4Mjc0NzRkMTIxNzEwNmY3IiwiaCI6Im11cm11cjY0In0=")


#  TomTom API key
API_KEY = os.getenv("TOMTOM_API_KEY", "CpIfmNNZcNZ81lmm9znSzdaaeVTAKLaI")

# URL
INCIDENTS_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails"
FLOW_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"


#printing selection

with open("coords.json", "r") as coords: # json Bry
    coords = json.load(coords)
    
print("Barangays in Santa Maria:\n")

def barangay_data(): # printing bry
    for count, brgy in enumerate(coords, start = 1):
        print(f"{count} | {brgy}")

def clearing(): #  clearing 
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')
    
    
# api gettign datas
def get_data(url, params):
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error:", resp.status_code, resp.text)
        return {}

#===========================================





def accesing_api(brgy_input) : 
    #accesing json's
    #point coord
    lat = coords[brgy_input]["latitude"]
    long = coords[brgy_input]["longitude"]
    #bounding box coord
    Bound_box = coords[brgy_input]["bounding_box"]
    min_lat = Bound_box["min_latitude"]
    max_lat = Bound_box["max_latitude"]
    min_lon = Bound_box["min_longditude"]
    max_lon = Bound_box["max_longditude"]
            
    # params ==========================
    Flow_params = {
        "point": f"{lat},{long}",  
        "key": API_KEY
    }
            
    flow_data = get_data(FLOW_URL, Flow_params)
            
    #example:
    #print("Current speed (km/h):", flow.get("currentSpeed"))
    Incidents_params = {
        "bbox": f"{min_lat},{max_lat},{min_lon},{max_lon}",  
        "key": API_KEY
    }
    Incidents_data = get_data(INCIDENTS_URL, Incidents_params)
            
            
    #example:
    # print("Type:", Incidents.get("incidentType"))
        
    return flow_data, Incidents_data


flow_data = Incidents_data = accesing_api()

# MAIN
while True:
    try:
        barangay_data()
        user_input = int(input("\nChoose a Barangay: "))
        brgy_input = list(coords)[user_input - 1]
        accesing_api(brgy_input)
        
        flow = flow_data.get("flowSegmentData", {})
        Incidents = Incidents_data.get(("incidents", []) or Incidents_data.get("features", []))
        
        
        if user_input <= 0: # Error loop
            clearing()
            continue
        else:  # main printing
            print(f"\n{brgy_input}, Latitude: {lat}, Longitude: {long}")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

# traffic indicator
        #     print("""
        # Traffic Level: ██░░░░░░░░ (NO Traffic)
        # Traffic Level: ██░░░░░░░░ (Ligth Traffic)
        # Traffic Level: ████░░░░░░ (Mild Traffic)
        # Traffic Level: ██████░░░░ (Moderate Traffic)
        # Traffic Level: ████████░░ (Heavy traffic)
        #       """)
        
        
        
    except(ValueError, IndexError): # ERRORS
        clearing()
        continue
        # print("Invalid Input. Pick a proper number")
       


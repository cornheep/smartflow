#MADE BY: GENON,JOMARI AND MAMAYSON GABRIEL LUIZ
#MADE ON  DECEMBER 27, 2025

# Community Traffic Monitoring System
#PROJECT PROPOSAL 
#GROUP SYTANX ERROR FROM BSCPE 1-1

#2025-2026
#MADE WITH LOVE <3

# --------------------------------------------------------------------------- #
# import openrouteservice
from rich.console import Console
from rich.table import Table
from rich import box
from tabulate import tabulate    
import itertools, sys, time, threading, os, json , requests

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

def accesing_api(brgy_input):
    global lat, long, flow_data, Incidents_data # global variables
    
    #accesing json's
    #point coord
    lat = coords[brgy_input]["main_coord"]["latitude"]
    long = coords[brgy_input]["main_coord"]["longitude"]
    
    
    #bounding box coord
    Bound_box = coords[brgy_input]["bounding_box"]
    min_lat = Bound_box["min_latitude"]
    max_lat = Bound_box["max_latitude"]
    min_lon = Bound_box["min_longitude"]
    max_lon = Bound_box["max_longitude"]
    # print(f"Bounding Box: {min_lon},{min_lat},{max_lon},{max_lat}")#for denugging
     
    # params ==========================
    Flow_params = {
        "point": f"{lat},{long}",  
        "key": API_KEY
    }
    flow_data = get_data(FLOW_URL, Flow_params)
    
    #example:
    # print("Current speed (km/h):", flow.get("currentSpeed"))
    Incidents_params = {
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",  
        "key": API_KEY
    }
    Incidents_data = get_data(INCIDENTS_URL, Incidents_params)
            
    #example:
    # print("Type:", Incidents.get("incidentType"))
    
#===========================================

# MAIN
while True:
    try:
        clearing()
        barangay_data()
        user_input = int(input("\nChoose a Barangay: "))
        barangays = list(coords)[user_input - 1]
        accesing_api(barangays)
        
        #getting data from api
        flow = flow_data.get("flowSegmentData", {})
        incidents = Incidents_data.get("incidents", []) or Incidents_data.get("features", [])
        
        
        if user_input <= 0: # Error loop
            clearing()
            continue
        else:  # main printing
            # print(f"\n{barangays}, Latitude: {lat}, Longitude: {long}")#debugging
            clearing()
            def spinner(stop_event):
                for c in itertools.cycle(['|', '/', '-', '\\']):
                    if stop_event.is_set():
                        break
                    sys.stdout.write('\r' + c)
                    sys.stdout.flush()
                    time.sleep(0.1)

            # Start spinner
            stop_event = threading.Event()
            t = threading.Thread(target=spinner, args=(stop_event,))
            t.start()

            # Simulate data loading
            time.sleep(2)  #seconds

            # Stop spinner
            stop_event.set()
            t.join()
            sys.stdout.write('\r' + ' ' * 20 + '\r')  # clear spinner line
                        
        # Spinner function
            
        console = Console()
        
        traffic_table = Table(title=f"{barangays.upper()}\nTRAFFIC FLOW DATA", box=box.ROUNDED)

        traffic_table.add_column("Traffic Metric", style="cyan", justify="left")
        traffic_table.add_column("Value", style="green", justify="center")

        traffic_table.add_row("Current Speed (km/h)", f"[green]{flow.get('currentSpeed')}km/h [/green]")
        traffic_table.add_row("Free Flow Speed (km/h)", f"{flow.get('freeFlowSpeed')}km/h")
        traffic_table.add_row("Confidence (%)", f"[blue]{round(flow.get('confidence')*100,2)}%[/blue]")
        traffic_table.add_row("Road Closure", "[red]HAVE ROAD CLOSURE![/red]" if flow.get("roadClosure") else "[green]No Road Closure[/green]")

        console.print(traffic_table)

        # -------------------------------
        # Incident Table
        # -------------------------------
        incident_table = Table(title="TRAFFIC INCIDENTS IN AREA", box=box.ROUNDED)

        incident_table.add_column("Incident Field", style="cyan", justify="left")
        incident_table.add_column("Value", style="yellow", justify="center")

        if incidents:
            for inc in incidents:
                props = inc.get("properties", {})
                incident_table.add_row("Type", f"[red]{props.get('incidentType')}[/red]")
                incident_table.add_row("Description", props.get("description"))
                incident_table.add_row("Severity", f"[yellow]{props.get('magnitudeOfDelay')}[/yellow]")
                incident_table.add_row("Start Time", f"[light_sea_green]{props.get('startTime')}[/light_sea_green]")
                incident_table.add_row("End Time", f"[light_sea_green]{props.get('endTime')}[/light_sea_green]")
                incident_table.add_row("Length (meters)", f"[dodger_blue3]{props.get('length')}[/dodger_blue3]")
                incident_table.add_row("Road Closed", "[red]HAVE ROAD CLOSURE![/red]" if props.get("roadClosed") else "[green]No Road Closure[/green]")
                incident_table.add_row("From", props.get("from"))
                incident_table.add_row("To", props.get("to"))
        else:
            incident_table.add_row("Incidents", "[green]No incidents found in this area[/green]")

        console.print(incident_table)

        time.sleep(3)
        break
            
        # # Debugging prints
        
            # print(f"Traffic Flow Segment Data: in {barangays}")
            # print("Current speed (km/h):", flow.get("currentSpeed"))
            # print("Free flow speed (km/h):", flow.get("freeFlowSpeed"))
            # print("Confidence:", flow.get("confidence"))
            # Road_Close = flow.get("roadClosure")
            # if Road_Close == True :
            #     print("RoadClosure: There is ROAD CLOSURE!") 
            # else:
            #     print("RoadClosure: There is no ROAD CLOSURE!")

            # if incidents:
            #     print("Traffic Incidents in Area:")
            #     for inc in incidents:
            #         props = inc.get("properties", {})
            #         print("--------------------------------------------------")
            #         print("Type:", props.get("incidentType"))
            #         print("Description:", props.get("description"))
            #         print("Severity:", props.get("magnitudeOfDelay"))
            #         print("Start Time:", props.get("startTime"))
            #         print("End Time:", props.get("endTime"))
            #         print("Length (meters):", props.get("length"))
            #         print("Road Closed:", props.get("roadClosed"))
                    
            #         inc_Road_Close = props.get("roadClosure")
            #         if inc_Road_Close == True :
            #             print("RoadClosure: There is ROAD CLOSURE!") 
            #         else:
            #             print("RoadClosure: There is no ROAD CLOSURE!")

            # else:
            #     print("No incidents found in this area.")
                    
        
    except(ValueError, IndexError): # ERRORS
        clearing()
        continue
  
       


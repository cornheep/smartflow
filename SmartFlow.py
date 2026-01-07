#MADE BY: GENON,JOMARI AND MAMAYSON GABRIEL LUIZ
#MADE ON  DECEMBER 27, 2025

# Community Traffic Monitoring System
#PROJECT PROPOSAL 
#GROUP SYTANX ERROR FROM BSCPE 1-1

#2025-2026
#MADE WITH LOVE <3

# --------------------------------------------------------------------------- #
# import openrouteservice                                       # for routing services (not used currently)                     
from rich.console import Console                                # table formatting
from rich.table import Table                                    # table formatting
from rich import box                                            # table formatting
from datetime import datetime , date                            # date and time
import itertools, sys, time, threading, os, json , requests     # other imports
from dotenv import load_dotenv
# client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdiYzQxMTY2NzVmZDQ2Mzc4Mjc0NzRkMTIxNzEwNmY3IiwiaCI6Im11cm11cjY0In0=")


#  TomTom API key
load_dotenv() 

API_KEY = os.getenv("API_KEY")
FLOW_URL = os.getenv("FLOW_URL")
INCIDENTS_URL = os.getenv("INCIDENTS_URL")

# 

#printing selection

with open("coords.json", "r") as coords:    # json Brgy
    coords = json.load(coords)
print("Barangays in Santa Maria:\n")


# printing bry
def barangay_data():             #NEED TO THIS TO TABLE!!
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

# accessing api function
def accesing_api(brgy_input):
    global lat, long, flow_data, Incidents_data # global variables
    
    #accesing json's
    #point coordinates
    lat = coords[brgy_input]["main_coord"]["latitude"]
    long = coords[brgy_input]["main_coord"]["longitude"]
    
    #bounding box coord format
    Bound_box = coords[brgy_input]["bounding_box"]
    min_lat = Bound_box["min_latitude"]
    max_lat = Bound_box["max_latitude"]
    min_lon = Bound_box["min_longitude"]
    max_lon = Bound_box["max_longitude"]
    # print(f"Bounding Box: {min_lon},{min_lat},{max_lon},{max_lat}")#for denugging
     
    # params ==========================
    
    #for current Flow
    Flow_params = {
        "point": f"{lat},{long}",   # geting the coordinates
        "key": API_KEY
    }
    flow_data = get_data(FLOW_URL, Flow_params)
    #example:
    # print("Current speed (km/h):", flow.get("currentSpeed"))
    
    #for Incidents
    Incidents_params = {
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",  # bounding box coordinates
        "key": API_KEY
    }
    Incidents_data = get_data(INCIDENTS_URL, Incidents_params)    
    #example:
    # print("Type:", Incidents.get("incidentType"))
    
#===========================================

# date and time
date = date.today()
time_now = datetime.now()
date = date.strftime("%d/%m/%Y")
time_now = time_now.strftime("%I:%M:%S %p")


# MAIN ===================================
while True:
    try:
        clearing()
        barangay_data()
        user_input = int(input("\nChoose a Barangay: ")) # user input
        barangays = list(coords)[user_input - 1]
        accesing_api(barangays)                          # accessing api function
        
        # data from api
        flow = flow_data.get("flowSegmentData", {})
        incidents = Incidents_data.get("incidents", []) or Incidents_data.get("features", [])
        
        if user_input <= 0: # Error loop
            clearing()
            continue
        
        else:  # main printing
            # print(f"\n{barangays}, Latitude: {lat}, Longitude: {long}")#debugging
            clearing() 
            def spinner(stop_event): # loding function
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

            #  loading
            time.sleep(2)  #seconds

            # Stop spinner
            stop_event.set()
            t.join()
            sys.stdout.write('\r' + ' ' * 20 + '\r')  # clear spinner line
                        
        # -------------------------------
        # Traffic Flow Table
        # -------------------------------
         
        console = Console() # accessing the imported console
        
        traffic_table = Table(title=f"{barangays.upper()}\nTRAFFIC FLOW DATA", box=box.ROUNDED)

        traffic_table.add_column("Traffic Metric", style="cyan", justify="left")
        traffic_table.add_column("Value", style="green", justify="center")

        traffic_table.add_row("Current Date", f"[green]{date}[/green]")
        traffic_table.add_row("Current Time", f"[green]{time_now}[/green]")
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
            accident_found = False
            for inc in incidents:
                props = inc.get("properties", {})
                if props.get("incidentType") == "ACCIDENT":
                    accident_found = True
                    incident_table.add_row("Type", f"[red]{props.get('incidentType')}[/red]")
                    incident_table.add_row("Description", props.get("description") or "N/A")
                    incident_table.add_row("Severity", f"[yellow]{props.get('magnitudeOfDelay')}[/yellow]")
                    incident_table.add_row("Start Time", f"[light_sea_green]{props.get('startTime')}[/light_sea_green]")
                    incident_table.add_row("End Time", f"[light_sea_green]{props.get('endTime')}[/light_sea_green]")
                    incident_table.add_row("Length (meters)", f"[dodger_blue3]{props.get('length')}[/dodger_blue3]")
                    incident_table.add_row("Road Closed", "[red]HAVE ROAD CLOSURE![/red]" if props.get("roadClosed") else "[green]No Road Closure[/green]")
                    incident_table.add_row("From", props.get("from") or "N/A")
                    incident_table.add_row("To", props.get("to") or "N/A")

            # If no accidents were found, print a clear message
            if not accident_found:
                incident_table.add_row("Accidents", "[green]No accidents found in this area[/green]")
        else:
            # No incidents at all
            incident_table.add_row("Incidents", "[green]No incidents found in this area[/green]")

        console.print(incident_table)

        time.sleep(3)
        break
            
        # /simple prints
        
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
  
       


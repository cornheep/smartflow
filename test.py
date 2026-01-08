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
from datetime import datetime, date                             # date and time
import itertools, sys, time, threading, os, json, requests      # other imports

# client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdiYzQxMTY2NzVmZDQ2Mzc4Mjc0NzRkMTIxNzEwNmY3IiwiaCI6Im11cm11cjY0In0=")


#  TomTom API key
API_KEY = os.getenv("TOMTOM_API_KEY", "CpIfmNNZcNZ81lmm9znSzdaaeVTAKLaI")

# URL
INCIDENTS_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails"
FLOW_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"


#printing selection

with open("coords.json", "r") as coords_file:    # json Brgy
    coords = json.load(coords_file)
print("Barangays in Santa Maria:\n")


# printing bry
def barangay_data():             #NEED TO THIS TO TABLE!!
    for count, brgy in enumerate(coords, start=1):
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
current_date = date.today()
time_now = datetime.now()
current_date = current_date.strftime("%d/%m/%Y")
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
        
        # Debugging: print raw incident data
        #print(f"\n[DEBUG] Raw Incidents Data Keys: {list(Incidents_data.keys())}")
        #print(f"[DEBUG] Full Incidents Data: {Incidents_data}")
        #print(f"[DEBUG] Number of Incidents Found: {len(incidents)}")
        #if incidents:
        #    print(f"[DEBUG] First Incident Structure: {incidents[0]}\n")
        
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

        traffic_table.add_row("Current Date", f"[green]{current_date}[/green]")
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
            for inc in incidents:
                # extract info from geoJSON format
                props = inc.get("properties", {})
                geom = inc.get("geometry", {})
                
                # get category from API
                icon_cat = props.get("iconCategory", 0)
                
                # category
                incident_types = {
                    0: "Unknown", 1: "Accident", 2: "Fog", 3: "Dangerous Conditions",
                    4: "Rain", 5: "Ice", 6: "Traffic Jam", 7: "Lane Closed",
                    8: "Road Closed", 9: "Road Works", 10: "Wind", 11: "Flooding",
                    13: "Cluster", 14: "Broken Down Vehicle"
                }
                incident_type = incident_types.get(icon_cat, f"Unknown Category {icon_cat}")
                
                # default description from API
                description = props.get("description", None)
                if not description:
                    # fallback descriptions if API doesn't provide one
                    fallback_descriptions = {
                        0: "Traffic condition detected in area",
                        1: "Vehicle collision causing delays",
                        2: "Low visibility conditions",
                        3: "Hazardous road conditions present",
                        4: "Wet road conditions",
                        5: "Icy/slippery road surface",
                        6: "Heavy traffic congestion",
                        7: "Reduced lane capacity",
                        8: "Road completely blocked",
                        9: "Construction/maintenance work in progress",
                        10: "Strong wind conditions",
                        11: "Flooded area - avoid if possible",
                        14: "Disabled vehicle blocking traffic"
                    }
                    description = fallback_descriptions.get(icon_cat, "Traffic condition detected in area")
                
                delay_seconds = props.get("delay", None)
                
                # magnitude of incedent
                magnitude = props.get("magnitude", props.get("magnitudeOfDelay", None))
                magnitude_map = {
                    0: "Unknown", 1: "Minor", 2: "Moderate", 3: "Major", 4: "Indefinite"
                }
                
                if magnitude is not None:
                    severity = magnitude_map.get(magnitude, "Unknown")
                else:
                    # fallback severity based on incident type
                    severity_map = {
                        0: "Unknown", 1: "High", 2: "Medium", 3: "High",
                        4: "Low", 5: "Medium", 6: "Medium", 7: "Medium",
                        8: "Critical", 9: "Low to Medium", 10: "Low", 
                        11: "High", 14: "Medium"
                    }
                    severity = severity_map.get(icon_cat, "Unknown")
                
                # ---- wag na 'to, kukuha nanaman ng bagong endpoint e di aabot sa oras
                # Get start and end times from API
                # start_time = props.get("startTime", "Currently Active")
                # end_time = props.get("endTime", props.get("end_date", "Monitoring..."))
                
                # Get length from API or calculate from coordinates
                length_meters = props.get("length", None)
                if length_meters is None:
                    incident_coords = geom.get("coordinates", [])
                    num_points = len(incident_coords) if incident_coords else 0
                    length_meters = num_points * 10  # Rough estimate
                    length_display = f"~{length_meters}m ({num_points} points)"
                else:
                    length_display = f"{length_meters}m"
                
                road_closed = props.get("roadClosed", False) or (icon_cat == 8)
                
                # Build severity display with delay info
                severity_display = severity
                if delay_seconds:
                    delay_minutes = delay_seconds // 60
                    severity_display = f"{severity} (Delay: {delay_minutes} min)"
                
                incident_table.add_row("Incident Type", f"[red]{incident_type}[/red]")
                incident_table.add_row("Description", f"[yellow]{description}[/yellow]")
                incident_table.add_row("Severity Level", f"[yellow]{severity_display}[/yellow]")
                incident_table.add_row("Affected Length", f"[dodger_blue3]{length_display}[/dodger_blue3]")
                incident_table.add_row("Road Status", "[red]ROAD CLOSED![/red]" if road_closed else "[green]Road Open - Caution Advised[/green]")
                incident_table.add_row("From", props.get("from"))
                incident_table.add_row("To", props.get("to"))
        else:
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
    
    except (ValueError, IndexError, KeyError) as e:
        print(f"\nInvalid input. Please try again.")
        time.sleep(2)
        continue
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        time.sleep(2)
        continue

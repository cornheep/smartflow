#MADE BY: GENON,JOMARI AND MAMAYSON GABRIEL LUIZ
#MADE ON  DECEMBER 27, 2025

# Community Traffic Monitoring System
#PROJECT PROPOSAL 
#GROUP SYTANX ERROR FROM BSCPE 1-1

#2025-2026
#MADE WITH LOVE <3 mas mahal ko sarili ko 

# --------------------------------------------------------------------------- #
from rich.console import Console
from rich.table import Table
from rich import box                                            
from datetime import datetime , date                            
import itertools, sys, time, threading, os, json , requests     
from dotenv import load_dotenv

#keys
load_dotenv() 
API_KEY = os.getenv("API_KEY")
FLOW_URL = os.getenv("FLOW_URL")
INCIDENTS_URL = os.getenv("INCIDENTS_URL")

#printing selection
with open("coords.json", "r") as coords:    
    coords = json.load(coords)
print("Barangays in Santa Maria:\n")

# printing bry
def barangay_data():
    for count, brgy in enumerate(coords, start = 1):
        print(f"{count} | {brgy}")

#  clearing 
def clearing(): 
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

# accessing api function
def accesing_api(brgy_input):
    global lat, long, flow_data, Incidents_data , FIELDS 
    
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
    
#COORDINATES
#point coordinates
    lat = coords[brgy_input]["main_coord"]["latitude"]
    long = coords[brgy_input]["main_coord"]["longitude"]
    
#bounding box coord 
    Bound_box = coords[brgy_input]["bounding_box"]
    min_lat = Bound_box["min_latitude"]
    max_lat = Bound_box["max_latitude"]
    min_lon = Bound_box["min_longitude"]
    max_lon = Bound_box["max_longitude"]  
       
# params ==========================

#for current Flow
    Flow_params = {
        "point": f"{lat},{long}",
        "key": API_KEY
    }
    flow_data = get_data(FLOW_URL, Flow_params)
    
#for Incidents
    Incidents_params = {
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",
        # "bbox": "120.89,14.49,121.21,14.81",  #FOR fix coordinates testing
        "key": API_KEY,
        "fields": FIELDS,
        "language": "en-GB",
        "timeValidityFilter": "present"
    }
    Incidents_data = get_data(INCIDENTS_URL, Incidents_params)    
 
# API'S CALL TYPES 
#INCIDENT TYPES 
def api_types(props):       
    global delay_severity, incident_severity, icon_cat, severity_map,  incident_type, magnitude_map, description, severity_display, length_fmt, delay_fmt, start_fmt, end_fmt
    
    icon_cat = props.get("iconCategory", 0)
    
    incident_types = {
                        0: "Unknown", 1: "Accident", 2: "Fog", 3: "Dangerous Conditions",
                        4: "Rain", 5: "Ice", 6: "Traffic Jam", 7: "Lane Closed",
                        8: "Road Closed", 9: "Road Works", 10: "Wind", 11: "Flooding",
                        13: "Cluster", 14: "Broken Down Vehicle"
                    }   
    incident_type = incident_types.get(icon_cat, f"Unknown Category {icon_cat}")

#MAGNITUDE TYPES
    magnitude = props.get("magnitude", props.get("magnitudeOfDelay", None))
    magnitude_map = {
        0: "Unknown", 1: "Minor", 2: "Moderate", 3: "Major", 4: "Indefinite"
    }
    
    severity_map = {
        0: "Unknown", 1: "High", 2: "Medium", 3: "High",
        4: "Low", 5: "Medium", 6: "Medium", 7: "Medium",
        8: "Critical", 9: "Low to Medium", 10: "Low", 
        11: "High", 14: "Medium"
    }
    if magnitude is not None:
        delay_severity = magnitude_map.get(magnitude, "Unknown")
    else:
        delay_severity = "Unknown"

    incident_severity = severity_map.get(icon_cat, "Unknown")

#DESCRIPTION TYPES
    description = props.get("description", None)
    if not description:
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
        description = fallback_descriptions.get(props.get("iconCategory"), "No description available")
    
#API TIME FORMATTING
    def format_time(ts): 

        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                return dt.strftime("%m/%d/%y %I:%M %p") #DATE FORMAT
            except Exception:
                return ts
        return "N/A"

    # Format length 
    length_m = props.get("length")
    length_fmt = f"{length_m:.2f} m" if length_m is not None else "N/A"

    # Format Seconds
    delay_s = props.get("delay")
    if delay_s is not None:
        minutes = delay_s // 60
        seconds = delay_s % 60
        delay_fmt = f"{minutes:02d}:{seconds:02d} Minutes"
    else:
        delay_fmt = "N/A"

    # Format start and end times
    start_fmt = format_time(props.get("startTime"))
    end_fmt = format_time(props.get("endTime"))
   
def loading_animation():  # loading animation    
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
            sys.stdout.write('\r' + ' ' * 20 + '\r')
               
# end of FUNCTIONS=================================
      
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
        
        else:  # main printing begins here
            clearing() 
            loading_animation()
        
# ============================================================

#   PRINTING TABLES

        # -------------------------------
        # Traffic Flow Table
        # -------------------------------
         
        console = Console() 
        
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

        incident_table = Table(title=f"TRAFFIC INCIDENTS IN AREA\n TOTAL INCIDENTS FOUND: {len(incidents)}", box=box.ROUNDED)
        incident_table.add_column("Incident Field", style="cyan", justify="left")
        incident_table.add_column("Value", style="yellow", justify="center")
        
        if incidents:
            for i, inc in enumerate(incidents, start=1):
                accident_found = True
                props = inc.get("properties", {})
                api_types(props)
                incident_table.add_row("Incident No#", f"[red]{i}[/red]")
                incident_table.add_row("","" )  
                
                incident_table.add_row("Type", f"[red]{incident_type}[/red]")
                incident_table.add_row("Description", f"[yellow]{description}[/yellow]")
                for event in props.get("events", []):
                    incident_table.add_row("events", f"{event.get('description')}")
                
                incident_table.add_row("Delay Severity", f"[yellow]{delay_severity}[/yellow]")
                incident_table.add_row("Severity Level", f"[yellow]{incident_severity}[/yellow]")

                incident_table.add_row("Delayed Time", f"[dodger_blue3]{delay_fmt}[/dodger_blue3]")
                
                incident_table.add_row("Status", f"[yellow]{props.get('timeValidity')}[/yellow]")
               
                incident_table.add_row("Start Time", f"[light_sea_green]{start_fmt}[/light_sea_green]")
                incident_table.add_row("End Time", f"[light_sea_green]{end_fmt}[/light_sea_green]")
               
                incident_table.add_row("Length (meters)", f"[dodger_blue3]{length_fmt}[/dodger_blue3]")
                incident_table.add_row("Road Closed", "[red]HAVE ROAD CLOSURE![/red]" if props.get("roadClosed") else "[green]No Road Closure[/green]")
               
                incident_table.add_row("From", props.get("from") or "N/A")
                incident_table.add_row("To", props.get("to") or "N/A")
                
                incident_table.add_row("Probability of Occurrence", f"[yellow]{props.get('probabilityOfOccurrence')}[/yellow]")

                incident_table.add_row("","" )             
                incident_table.add_row(f"[white]-----------[/white]",f"[white]-----------[/white]") 
                incident_table.add_row("","" )  

        else:
            # No incidents at all
            incident_table.add_row("Incidents", "[green]No incidents found in this area[/green]")
        print("\n")
        
        console.print(incident_table)
        while True:
                user_choice = input("Would you like to monitor another barangay? (yes/no): ").strip().lower()
                if user_choice in ["yes", "y"]:
                    clearing()
                    break
                elif user_choice in ["no", "n"]:
                    clearing()
                    print("Exiting the program. Stay safe!")
                    sys.exit(0)
                else:
                    continue        
            
    except(ValueError, IndexError):
        clearing()
        continue
  
       


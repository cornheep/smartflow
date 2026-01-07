from rich.console import Console
from rich.table import Table
from rich import box

# Mock data
barangays = "Barangay 123"
date = "2026-01-07"
time_now = "23:36"

flow = {
    "currentSpeed": 45,
    "freeFlowSpeed": 60,
    "confidence": 0.925,
    "roadClosure": False
}

incidents = [
    {
        "properties": {
            "incidentType": "ACCIDENT",
            "description": "Minor collision near intersection",
            "magnitudeOfDelay": 2,
            "startTime": "2026-01-07T22:45:00",
            "endTime": "2026-01-07T23:15:00",
            "length": 150,
            "roadClosed": False,
            "from": "Main St.",
            "to": "2nd Ave."
        }
    }
]

console = Console()

# -------------------------------
# Traffic Flow Table
# -------------------------------
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
    accident_found = True
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

console.print(incident_table)


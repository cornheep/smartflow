import json
import openrouteservice

with open("coords.json", "r") as coords:
    coords = json.load(coords)

print("Barangays in Santa Maria:\n")

for count, brgy in enumerate(coords, start = 1):
    print(f"{count} | {brgy}")

try:
    user_input = int(input("\nChoose a Barangay: "))
    brgy_input = list(coords)[user_input - 1]
    lat = coords[brgy_input]["latitude"]
    long = coords[brgy_input]["longitude"]

    print(f"\n{brgy_input}, Latitude: {lat}, Longitude: {long}")

    client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdiYzQxMTY2NzVmZDQ2Mzc4Mjc0NzRkMTIxNzEwNmY3IiwiaCI6Im11cm11cjY0In0=")

except(ValueError, IndexError):
    print("Invalid Input. Pick a proper number")


import json
import openrouteservice
import os
# client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdiYzQxMTY2NzVmZDQ2Mzc4Mjc0NzRkMTIxNzEwNmY3IiwiaCI6Im11cm11cjY0In0=")

with open("coords.json", "r") as coords:
    coords = json.load(coords)

print("Barangays in Santa Maria:\n")


def barangay_data():
    for count, brgy in enumerate(coords, start = 1):
        print(f"{count} | {brgy}")

def clearing():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')




while True:
    try:
        barangay_data()
        user_input = int(input("\nChoose a Barangay: "))
        brgy_input = list(coords)[user_input - 1]
        lat = coords[brgy_input]["latitude"]
        long = coords[brgy_input]["longitude"]
        if user_input <= 0:
            clearing()
            continue
        else:
            print(f"\n{brgy_input}, Latitude: {lat}, Longitude: {long}")

# traffic indicator
        #     print("""
        # Traffic Level: ██░░░░░░░░ (NO Traffic)
        # Traffic Level: ██░░░░░░░░ (Ligth Traffic)
        # Traffic Level: ████░░░░░░ (Mild Traffic)
        # Traffic Level: ██████░░░░ (Moderate Traffic)
        # Traffic Level: ████████░░ (Heavy traffic)
        #       """)
    except(ValueError, IndexError):
        clearing()
        continue
        # print("Invalid Input. Pick a proper number")
       


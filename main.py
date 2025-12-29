import json

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

except(ValueError, IndexError):
    print("putangina mo")


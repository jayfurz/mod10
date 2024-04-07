import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "821dd501347846ab9f408d2b6365165d"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, "Accept": "*/*"}

################################################################################

app = Flask(__name__)


# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Send a GET request to the WMATA Incidents API.
    response = requests.get(INCIDENTS_URL, headers=headers)
    # Convert the API response to JSON format.
    data = response.json()
    # Initialize an empty list to store matching incidents.
    incidents = []

    # Iterate over each incident in the 'ElevatorIncidents' list from the API response.
    for incident in data.get('ElevatorIncidents', []):
        # Check if the incident's 'UnitType' matches the requested 'unit_type', ignoring case
        # and removing the trailing "s" to handle both singular and plural forms.
        if incident['UnitType'].lower() == unit_type.lower().strip("s"):
            # If it matches, append a dictionary with the required fields to the 'incidents' list.
            incidents.append({
                "StationCode": incident['StationCode'],  # Station code where the incident occurred.
                "StationName": incident['StationName'],  # Name of the station.
                "UnitName": incident['UnitName'],        # Name of the unit (elevator/escalator) affected.
                "UnitType": incident['UnitType'],        # Type of the unit (ELEVATOR/ESCALATOR).
            })
    # Return the list of matching incidents as a JSON-formatted string.
    return json.dumps(incidents)


if __name__ == "__main__":
    app.run(debug=True)

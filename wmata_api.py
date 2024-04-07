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
    response = requests.get(INCIDENTS_URL, headers=headers)
    data = response.json()
    incidents = []

    for incident in data.get('ElevatorIncidents', []):
        if incident['UnitType'].lower() == unit_type.lower().strip("s"):
            incidents.append({
                "StationCode": incident['StationCode'],
                "StationName": incident['StationName'],
                "UnitName": incident['UnitName'],
                "UnitType": incident['UnitType'],
            })
    return json.dumps(incidents)


if __name__ == "__main__":
    app.run(debug=True)

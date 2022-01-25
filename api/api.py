from usgs.usgs_api import Query
from flask import Flask, request
import json
from datetime import datetime, timedelta
import os


# Info that all endpoints have in common
minmagnitude = "2.0"
# For searching states
states = {"AL":"Alabama", "AK":"Alaska","AZ":"Arizona","AR":"Arkansas",
"CA":"California","CO":"Clorado","CT":"Connecticut","DE":"Delaware",
"FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois",
"IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Lousiana",
"ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan",
"MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana",
"NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
"NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota",
"OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island",
"SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas",
"UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia",
"WI":"Wisconsin","WY":"Wyoming"}

# San Francisco Bay rectangular coordinates
sf_coordinates = {"maxlatitude":38.294, "minlatitude":37.235,
                        "maxlongitude":-121.675, "minlongitude":-122.835}
# Query object to make requests on USGS
query_obj = Query()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route("/first", methods=["GET"])
def do_1st_endpoint():

    # Get arguments
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")

    # Get data from the Request on the url
    query = query_obj.get_json_data(starttime=starttime,
        endtime=endtime, minmagnitude=minmagnitude, maxlatitude=sf_coordinates["maxlatitude"],
        minlatitude=sf_coordinates["minlatitude"], maxlongitude=sf_coordinates["maxlongitude"],
        minlongitude=sf_coordinates["minlongitude"])

    # String to json
    data = json.loads(query)

    # In case there were no earthquakes
    if data["features"] == []:
        return f"Fortunately there was no seismic activity in the San Francisco Bay during the {starttime} and the {endtime}"

    # Make the data more readable
    data_str = json.dumps(data, indent=2)

    return data_str

@app.route("/second", methods=["GET"])
def do_2nd_endpoint():

    # Get arguments
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")

    # Get data from the Request on the url
    query = query_obj.get_json_data(starttime=starttime,
        endtime=endtime, minmagnitude=minmagnitude, maxlatitude=sf_coordinates["maxlatitude"],
        minlatitude=sf_coordinates["minlatitude"], maxlongitude=sf_coordinates["maxlongitude"],
        minlongitude=sf_coordinates["minlongitude"], minfelt=10)

    # String to json
    data = json.loads(query)

    # In case there were no earthquakes
    if data["features"] == []:
        return f"Fortunately there was no seismic activity in the San Francisco Bay during the {starttime} and the {endtime}"

    # Make the data more readable
    data_str = json.dumps(data, indent=2)

    return data_str

@app.route("/third", methods=["GET"])
def do_3rd_endpoint():

    # Get arguments
    state = request.args.get("state")

    if state not in states:
        return "Invalid state"

    # Get dates format starting from yesterday until today
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    starttime = yesterday.strftime('%Y-%m-%d')
    endtime = today.strftime('%Y-%m-%d')

    # Get data from the Request on the url
    query = query_obj.get_json_data(starttime=starttime,
            endtime=endtime, minmagnitude=minmagnitude)

    data = json.loads(query)

    # Some places don't have the abbreviation
    state_name = states[state]

    results = []

    # Filter by state and tsunami occurence
    for feature in data["features"]:
        # tsunami info
        tsunami = feature["properties"]["tsunami"]
        # place info
        place = feature["properties"]["place"]

        # Avoid Errors
        if place is None or tsunami is None:
            continue

        #elif state in place or state_name in place:   This 2 comments were done just to get some data
        #elif (tsunami == 0):                           because fortunately there were no tsunamis in the US
        elif (state in place or state_name in place) and tsunami == 1:
            results.append(feature)

    if results == []:
        return "No earthquakes found with the given parameters"

    # Make the data more readable
    results = json.dumps(results, indent=2)
    return results

# This method will retrieve all earthquakes M2.0+ during a specific time range for any given US state
@app.route("/bonus", methods=["GET"])
def bonus():

    # Get arguments
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    state = request.args.get("state")

    # Get data from the Request on the url
    query = query_obj.get_json_data(starttime=starttime,
        endtime=endtime, minmagnitude=minmagnitude)

    data = json.loads(query)

    # Some places don't have the abbreviation
    state_name = states[state]

    results = []

    # Filter by state and tsunami occurence
    for feature in data["features"]:
        # place info
        place = feature["properties"]["place"]

        # Avoid Errors
        if place is None:
            continue

        elif state in place or state_name in place:
            results.append(feature)

    if results == []:
        return "No earthquakes found with the given parameters"

    # Make the data more readable
    results = json.dumps(results, indent=2)
    return results

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

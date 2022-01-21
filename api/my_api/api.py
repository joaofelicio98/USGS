from usgs.usgs_api import Query
#from flask import Flask
import json
from datetime import datetime, timedelta

class API():

    def __init__(self):
        # Info that all endpoints have in common
        self.format = "geojson"
        self.minmagnitude = "2.0"
        # For searching states
        self.states = {"AL":"Alabama", "AK":"Alaska","AZ":"Arizona","AR":"Arkansas",
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
        self.sf_coordinates = {"maxlatitude":38.294, "minlatitude":37.235,
                                "maxlongitude":122.835, "minlongitude":121.675}

        self.query_obj = Query()

    def do_1st_endpoint(self, starttime, endtime):

        # Get data from the Request on the url
        query = self.query_obj.get_json_data(format=self.format, starttime=starttime,
            endtime=endtime, minmagnitude=self.minmagnitude, maxlatitude=self.sf_coordinates["maxlatitude"],
            minlatitude=self.sf_coordinates["minlatitude"], maxlongitude=self.sf_coordinates["maxlongitude"],
            minlongitude=self.sf_coordinates["minlongitude"])

        # String to json
        data = json.loads(query)

        # Make the data more readable
        data_str = json.dumps(data, indent=2)

        print(data_str)

    def do_2nd_endpoint(self, starttime, endtime):

        # Get data from the Request on the url
        query = self.query_obj.get_json_data(format=self.format, starttime=starttime,
            endtime=endtime, minmagnitude=self.minmagnitude, maxlatitude=self.sf_coordinates["maxlatitude"],
            minlatitude=self.sf_coordinates["minlatitude"], maxlongitude=self.sf_coordinates["maxlongitude"],
            minlongitude=self.sf_coordinates["minlongitude"], minfelt=10)

        # String to json
        data = json.loads(query)

        # Make the data more readable
        data_str = json.dumps(data, indent=2)

        print(data_str)


    def do_3rd_endpoint(self, state):

        # Get dates format starting from yesterday until today
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        starttime = yesterday.strftime('%Y-%m-%d')
        endtime = today.strftime('%Y-%m-%d')

        # Get data from the Request on the url
        query = self.query_obj.get_json_data(format=self.format, starttime=starttime,
                endtime=endtime, minmagnitude=self.minmagnitude)

        data = json.loads(query)

        # Some places don't have the abbreviation
        state_name = self.states[state]

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

        # Make the data more readable
        results = json.dumps(results, indent=2)
        print(results)


# Do the Debugging
if __name__ == "__main__":
    api = API()
    #api.do_1st_endpoint(starttime="2014-01-01", endtime="2014-01-02")
    api.do_3rd_endpoint("AK")

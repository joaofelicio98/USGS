from usgs.usgs_api import Query
#from flask import Flask
import json

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

        query = self.query_obj.get_json_data(format=self.format, starttime=starttime,
            endtime=endtime, minmagnitude=self.minmagnitude, maxlatitude=self.sf_coordinates["maxlatitude"],
            minlatitude=self.sf_coordinates["minlatitude"], maxlongitude=self.sf_coordinates["maxlongitude"],
            minlongitude=self.sf_coordinates["minlongitude"])


        data = json.loads(query)

        data_str = json.dumps(data, indent=2)

        print(data_str)
        print()
        # Get place info
        #print(data["features"][0]["properties"]["place"])

    def do_2nd_endpoint(self, starttime, endtime):
        minfelt = 10

    def do_3rd_endpoint(self, state):
        state_name = self.states(state)


if __name__ == "__main__":
    api = API()
    api.do_1st_endpoint(starttime="2014-01-01", endtime="2014-01-02")

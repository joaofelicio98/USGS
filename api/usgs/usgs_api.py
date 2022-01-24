import requests
import pprint

# HTTP Requests needed
"""
GET  -> get data from earthquake usgs
"""

# My endpoint
"""
https://earthquake.usgs.gov/fdsnws/event/1/[METHOD[?PARAMETERS]]
"""

# What HTTP methods I need?
"""
I want the query method to get info
"""

class Query:

    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1/"
        self.method = "query" # the 3 endpoints will only use the query method
        self.format = "geojson" # I want to get only in json format

    # Do the requested query
    # kwargs contains all the parameters needed for the endpoint with the proper names
    def get_json_data(self, **kwargs):
        endpoint_path = f"format={self.format}"

        for key in kwargs:
            endpoint_path += f"&{key}={kwargs.get(key)}"

        url = f"{self.base_url}/{self.method}?{endpoint_path}"

        # Get data from the earthquake USGS API
        r = requests.get(url)

        # Return data string
        return r.text

#Testing
if __name__ == "__main__":
    new = Query()
    data = new.get_json_data(starttime="2014-01-01", endtime="2014-01-02", minmagnitude="2.0")
    pprint.pprint(data)

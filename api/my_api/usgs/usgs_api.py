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
        self.method = "query" # the 3 endpoint will only use the query method
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

"""
# TESTING

url = "http://jsonplaceholder.typicode.com/users"

user = input("Search by username: ")
queryURL = f"{url}?username={user}"

r = requests.get(queryURL)

userdata = json.loads(r.text)[0]

print(f"Name = {userdata['name']}")
print(f"Email = {userdata['email']}")
"""

"""
Useful things Requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)

r.url

payload = {'key1': 'value1', 'key2': ['value2', 'value3']}

r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)
https://httpbin.org/get?key1=value1&key2=value2&key2=value3



"""

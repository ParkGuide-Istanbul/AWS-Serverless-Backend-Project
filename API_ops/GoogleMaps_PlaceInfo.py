import GoogleMaps_PlaceID as gmpi
import requests
import smtplib

class google_maps_place_info:
    def __init__(self, dest_id):
        self.dest_id = dest_id
        self.api_key = "AIzaSyDHkfZhEbOlIDyYyx0FiXF5K28VATsiVL0"

    def get_place_info(self):
        url1 = "https://maps.googleapis.com/maps/api/place/details/json?&place_id="
        url2= "&key="
        r = requests.get(url1 + self.dest_id + url2 + self.api_key) 
        return (r.json()["result"]["geometry"]["location"]["lat"], 
                r.json()["result"]["geometry"]["location"]["lng"])

    def get_district_name(self):
        url1 = "https://maps.googleapis.com/maps/api/place/details/json?&place_id="
        url2= "&key="
        r = requests.get(url1 + self.dest_id + url2 + self.api_key) 
        return (r.json()["result"]["address_components"][3]["long_name"])
    



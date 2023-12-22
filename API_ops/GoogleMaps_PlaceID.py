import requests
import smtplib

class google_maps_place_id:
    def __init__(self, dest):
        self.dest = dest
        self.api_key = "AIzaSyDHkfZhEbOlIDyYyx0FiXF5K28VATsiVL0"
    def __str__(self):
        return self.get_place_id()
    def get_place_id(self):
        dest_fixed = self.dest.replace(" ","%20")
        url1 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
        url2= "&inputtype=textquery&key="
        r = requests.get(url1 + dest_fixed + url2 + self.api_key)
        return r.json()["candidates"][0]["place_id"]
    


destID = google_maps_place_id("ITU Maslak Türkiye")
print(destID)
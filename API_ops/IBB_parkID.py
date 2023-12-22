import requests
import smtplib

class ibb_parks_ID:
    def __init__(self, dest_id=None):
        if dest_id == None:
            self.dest_id = []
        else:
            self.dest_id = dest_id

    def get_place_info(self):
        url1 = "https://api.ibb.gov.tr/ispark/ParkDetay?id="
        park_info = []
        for i in range(len(self.dest_id)):
            r = requests.get(url1 + self.dest_id[i]) 
            park_info.append([r.json()[0]["parkID"],r.json()[0]["lat"],r.json()[0]["lng"],r.json()[0]["district"],r.json()[0]["parkName"]])
        return park_info

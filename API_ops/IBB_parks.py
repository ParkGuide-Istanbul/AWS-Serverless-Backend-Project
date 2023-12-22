import csv

class ParkFinder:
    parks_data = []

    @classmethod
    def load_parks(cls, csv_file):
        if not cls.parks_data: 
            with open(csv_file, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                cls.parks_data = list(csv_reader)

    @classmethod
    def search_by_district(cls, district_name):
        return [park['parkID'] for park in cls.parks_data if park['district'].lower() == district_name.lower()]


ParkFinder.load_parks('IBB_parks.csv') 
# park_ids = ParkFinder.search_by_district('your_district_name')
# print(park_ids)
import boto3
import requests
from boto3.dynamodb.conditions import Attr
import math
import time

api_key = "AIzaSyDHkfZhEbOlIDyYyx0FiXF5K28VATsiVL0"   

def get_travel_time(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "mode": "driving"  # Araba ile seyahat süresi için
    }

    response = requests.get(url, params=params)
    directions = response.json()

    if directions['status'] == 'OK':
        route = directions['routes'][0]
        leg = route['legs'][0]
        duration = leg['duration']
        distance = leg['distance']
        return duration['text'],distance['text']
    else:
        return "Yolculuk süresi hesaplanamadı."

def calculate_distance(lat1, lon1, lat2, lon2):
    # Derece cinsinden olan enlem ve boylamı metre cinsine çevirme faktörleri
    # İstanbul için bu faktörler yaklaşık olarak:
    lat_to_km = 110.574  # 1 derece enlem, kilometre cinsinden
    lon_to_km = 111.320 * math.cos(math.radians(lat1))  # 1 derece boylam, kilometre cinsinden

    # Enlem ve boylam farklarını hesapla ve kilometreye çevir
    delta_lat_km = (lat2 - lat1) * lat_to_km
    delta_lon_km = (lon2 - lon1) * lon_to_km

    # Pisagor teoremini uygula
    distance_km = math.sqrt(delta_lat_km**2 + delta_lon_km**2)
    return distance_km


def lambda_handler(event, context):
    # ı want to print whole execution time sn unit
    start_time = time.time()
    # İBB API'den park verilerini çek
    ibb_api_url = "https://api.ibb.gov.tr/ispark/Park"
    parks_data = requests.get(ibb_api_url).json()

    # Event'ten ilçe bilgisini al
    input_district = event.get("district")

    # DynamoDB'den ilçenin komşu ilçelerini çek
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Districts')
    response = table.get_item(Key={'Name': input_district})
    adjacent_districts = response['Item']['AdjacentDistricts']

    # İlçe ve komşu ilçeleri bir listeye dönüştür
    districts_to_filter = [input_district] + [district for district in adjacent_districts]

    table_parks = dynamodb.Table('Parks')
    scan_result = table_parks.scan(FilterExpression=Attr('state').eq('0'))
    inactive_park_ids = {item['id']for item in scan_result['Items']}

    # Filtreleme işlemi
    filtered_parks = []
    for park in parks_data:
        if (park['district'] in districts_to_filter and 
            park['isOpen'] == 1 and 
            park['emptyCapacity'] != 0 and 
            str(park['parkID']) not in inactive_park_ids):
            filtered_parks.append(park)

    input_lat = float(event.get("lat"))
    input_lng = float(event.get("lng"))

    for park in filtered_parks:
        park_lat = float(park['lat'])
        park_lng = float(park['lng'])
        park['distance'] = calculate_distance(input_lat, input_lng, park_lat, park_lng)

    sorted_filtered_parks = sorted(filtered_parks, key=lambda x: x['distance'])

    #ilk 20 i al

    sorted_filtered_parks = sorted_filtered_parks[:15]

    

    for park in sorted_filtered_parks:
        park['Time'],park['distance2'] = get_travel_time(f"{input_lat},{input_lng}", f"{park['lat']},{park['lng']}")
    print(sorted_filtered_parks)
    print("--- %s seconds ---" % (time.time() - start_time))
    return sorted_filtered_parks


lambda_handler({"district": "SARIYER","lat":"41.0416","lng":"28.8946"}, None)
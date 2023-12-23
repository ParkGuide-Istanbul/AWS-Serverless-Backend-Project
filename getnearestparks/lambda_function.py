import boto3
import requests
from boto3.dynamodb.conditions import Attr
import math
import time
import json
import jwt
SECRET_KEY = "Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F"
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


    header = event['headers']              #  json.loads(event['headers'])
    token = header['authorization-token']


    # Token yoksa veya boşsa hata dön
    if not token:
        return unauthorized_response('No token provided')

    try:
        # Token'ı decode et
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return unauthorized_response('Token expired')
    except jwt.InvalidTokenError:
        return unauthorized_response('Invalid token')
    

    try:
        body =json.loads(event['body'])            #   event['body']
        input_district = body['district']
        input_lat = float(body['lat'])
        input_lng = float(body['lng'])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request format'})
        }
    

    try:
        # İBB API'den park verilerini çekmeye çalış
        ibb_api_url = "https://api.ibb.gov.tr/ispark/Park"
        parks_data = requests.get(ibb_api_url).json()
    except requests.exceptions.RequestException:
        # Eğer hata oluşursa, verileri DynamoDB'den çek
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Parks_cache')
        response = table.scan()
        parks_data = response['Items']
        if not parks_data:
            return {
                'statusCode': 503,
                'body': json.dumps({'message': 'Failed to fetch park data from both API and cache'})
            }


    # Event'ten ilçe bilgisini al


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
            (park['isOpen'] == 1  or park['isOpen'] == '1') and 
            (park['emptyCapacity'] != 0 or park['emptyCapacity'] != '0') and 
            str(park['parkID']) not in inactive_park_ids):
            filtered_parks.append(park)



    for park in filtered_parks:
        park_lat = float(park['lat'])
        park_lng = float(park['lng'])
        park['distance'] = calculate_distance(input_lat, input_lng, park_lat, park_lng)

    sorted_filtered_parks = sorted(filtered_parks, key=lambda x: x['distance'])



    sorted_filtered_parks = sorted_filtered_parks[:10]

    for park in sorted_filtered_parks:
        park['Time'] = get_travel_time(str(input_lat) + "," + str(input_lng), str(park['lat']) + "," + str(park['lng']))[0]
        park['MapsURL'] = "https://www.google.com/maps/dir/?api=1&origin=" + str(input_lat) + "," + str(input_lng) + "&destination=" + str(park['lat']) + "," + str(park['lng']) + "&travelmode=driving"
    print(sorted_filtered_parks)

    return {
        'statusCode': 200,
        'body': json.dumps(sorted_filtered_parks, ensure_ascii=False)
    }


def unauthorized_response(message):
    return {
        'statusCode': 401,
        'body': json.dumps({'message': message})
    }


event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAzMzczMDg3fQ.ai9BbHLfzMua75HTACKcxnDVPk1oSZx4tPSUZo9xCCo",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
        "district": "KADIKÖY", 
        "lat": "40.9911", 
        "lng": "29.0270"
        
    }
        
}


response = lambda_handler(event, None)

print(response)
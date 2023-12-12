import json
import boto3
import requests
import jwt
import datetime
from botocore.exceptions import ClientError

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
parks_table = dynamodb.Table('Parks')
users_table = dynamodb.Table('Users')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'

def lambda_handler(event, context):
    # Token'ı Authorization header'ından al

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

    # Roller kontrolü
    roles = decoded_token.get('roles', [])
    if 'Admin' not in roles and 'ParkingSystemAdmin' not in roles:
        return unauthorized_response('Unauthorized: insufficient permissions')

    # İBB API'dan park bilgilerini al
    api_url = "https://api.ibb.gov.tr/ispark/Park"
    response = requests.get(api_url)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'message': 'Failed to fetch park data'})
        }

    park_data = response.json()

    response = parks_table.scan()
    parks_data = response.get('Items', [])

    # Park ID'sine göre state bilgisini bir sözlükte sakla
    park_states = {park['id']: park.get('state', 'unknown') for park in parks_data}

    # Her park için state bilgisini DynamoDB'den al ve ekle
    for park in park_data:
        try:
            park_id = str(park['parkID'])
            park['state'] = park_states.get(park_id, 'unknown')
        except ClientError as e:
            print(e.response['Error']['Message'])
            park['state'] = 'error'

    return {
        'statusCode': 200,
        'body': json.dumps(park_data)
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
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDI4MTIzfQ.B7f7J-DPULjvJCZKdZv8hD3GIIhOnvF5xdb794TumLA",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
        
    }
        
}


response = lambda_handler(event, None)

print(response)
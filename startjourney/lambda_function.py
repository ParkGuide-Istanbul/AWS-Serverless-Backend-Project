import boto3
import json
import jwt
from botocore.exceptions import ClientError
from uuid import uuid4
# from cryptography.fernet import Fernet

# Anahtar oluştur
# key = b'nmRt2Bxw3KblYQNlzAfFlisoejkJ4Tfv4eQlOuyegw8='
# key = Fernet.generate_key()
# print(key)

# Fernet örneği oluştur
# fernet = Fernet(key)

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
journey_table = dynamodb.Table('Journeys')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # Gerçek uygulamada güvenli bir şekilde saklayın

def encrypt_data(data):
    """Verilen veriyi şifrele."""
    return fernet.encrypt(data.encode()).decode()

def check_active_journey(user):
    """Belirtilen kullanıcının aktif yolculuğunu kontrol et."""
    response = journey_table.scan(
        FilterExpression='#usr = :user and IsFinished = :isFinished',
        ExpressionAttributeNames={
            '#usr': 'User'  # 'User' için takma ad
        },
        ExpressionAttributeValues={
            ':user': user,
            ':isFinished': '0'
        }
    )
    return 'Items' in response and len(response['Items']) > 0

def lambda_handler(event, context):
    # Token'ı Authorization header'ından al
    header = event['headers']
    token = header.get('authorization-token')

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

    # Kullanıcı bilgisini al
    user = decoded_token.get('username')
    if not user:
        return unauthorized_response('User not found in token')

    # Request body'den yolculuk bilgilerini al
    try:
        body = event['body']          #json.loads(event['body'])   
        starting = body['starting']
        destination = body['destination']
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request format'})
        }
    
    if check_active_journey(user):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'User already has an active journey'})
        }

    # Yeni bir Journey kaydı oluştur
    new_journey_id = str(uuid4())  # Benzersiz bir ID oluştur
    new_journey = {
        'JourneyId': str(uuid4()),
        'User': user,
        'StartingDistrict': starting['startingdistrict'],
        'StartingLocation(lat-lng)': f"{starting['startinglat']}-{starting['startinglng']}",
        'DestinationDistrict': destination['destinationdistrict'],
        'DestinationLocation(lat-lng)': f"{destination['destinationlat']}-{destination['destinationlng']}",
        'IsFinished': '0'
    }

    try:
        # DynamoDB'ye kaydet
        journey_table.put_item(Item=new_journey)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error creating new journey'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Journey started successfully', 'JourneyId': new_journey_id})
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
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiQWRtaW4iLCJTdGFuZGFydFVzZXIiXSwiZXhwIjoxNzAzNDA0NTgzfQ.6VWgyEulr6oFuleeydx5mySuA5KrVKiTuEDaHxiYhuU",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
           "starting": {
                "startingdistrict": "KADIKÖY",
                "startinglat": "40.9911",
                "startinglng": "29.0270"
        },
            "destination":{
                "destinationdistrict": "SARIYER",
                "destinationlat": "40.9911",
                "destinationlng": "29.0270"
        }
    
        
    }
        
}


response = lambda_handler(event, None)

print(response)
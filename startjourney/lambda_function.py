import json
import boto3
import jwt
from botocore.exceptions import ClientError
from uuid import uuid4
from cryptography.fernet import Fernet

# Anahtar oluştur


# Fernet örneği oluştur
fernet = Fernet(key)

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
journey_table = dynamodb.Table('Journey')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # Gerçek uygulamada güvenli bir şekilde saklayın

def encrypt_data(data):
    """Verilen veriyi şifrele."""
    return fernet.encrypt(data.encode()).decode()

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
        body = json.loads(event['body'])
        starting = body['starting']
        destination = body['destination']
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request format'})
        }

    # Yeni bir Journey kaydı oluştur
    new_journey_id = str(uuid4())  # Benzersiz bir ID oluştur
    new_journey = {
        'JourneyId': str(uuid4()),
        'User': user,
        'StartingDistrict': encrypt_data(starting['startingdistrict']),
        'StartingLocation(lat-lng)': encrypt_data(f"{starting['startinglat']}-{starting['startinglng']}"),
        'DestinationDistrict': encrypt_data(destination['destinationdistrict']),
        'DestinationLocation(lat-lng)': encrypt_data(f"{destination['destinationlat']}-{destination['destinationlng']}"),
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

import boto3
import json
import jwt
from botocore.exceptions import ClientError
from collections import Counter

# AWS DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
journey_table = dynamodb.Table('Journeys')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # Güvenli bir şekilde saklayın

def lambda_handler(event, context):
    # Token'ı Authorization header'ından al
    header = event['headers']
    token = header.get('authorization-token')

    # Token kontrolü
    if not token:
        return unauthorized_response('No token provided')

    try:
        # Token'ı decode et
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return unauthorized_response('Token expired')
    except jwt.InvalidTokenError:
        return unauthorized_response('Invalid token')

    # Kullanıcı bilgisini token'dan al
    user = decoded_token.get('username')
    if not user:
        return unauthorized_response('User not found in token')

    # Kullanıcının journey'lerini sorgula
    try:
        response = journey_table.scan(
            FilterExpression='#usr = :user',
            ExpressionAttributeNames={'#usr': 'User'},  # 'User' için takma ad
            ExpressionAttributeValues={':user': user}
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching journeys'})
        }

    # Hedef konumları say
    destinations = Counter()
    for item in response.get('Items', []):
        destination = item['DestinationLocation(lat-lng)']
        district = item['DestinationDistrict']
        destinations[(destination, district)] += 1

    # En çok ziyaret edilen 4 hedefi bul
    top_destinations = destinations.most_common(4)
    result = [{'lat-lng': dest[0], 'district': dest[1]} for dest, _ in top_destinations]

    return {
        'statusCode': 200,
        'body': json.dumps(result)
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
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiQWRtaW4iLCJTdGFuZGFydFVzZXIiXSwiZXhwIjoxNzAzODU1MTg4fQ.YlJwX5H6tcZ_W4nWyeYpOfS8oRjdZVVwyrZop-5h0F0",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    }

}


# response = lambda_handler(event, None)

# print(response)

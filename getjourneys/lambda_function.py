import json
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import jwt

# Veritabanı ayarları
dynamodb = boto3.resource('dynamodb')
journeys_table = dynamodb.Table('Journeys')  # 'Journeys' tablosunu tanımla

SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # JWT için gizli anahtarınız

def unauthorized_response(message):
    return {
        'statusCode': 401,
        'body': json.dumps({
            'statusCode': 401,
            'message': message
        })
    }

def lambda_handler(event, context):
    # Token'ı Authorization header'ından al
    header = event['headers']
    token = header.get('authorization-token')

    if not token:
        return unauthorized_response('No token provided')

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return unauthorized_response('Token expired')
    except jwt.InvalidTokenError:
        return unauthorized_response('Invalid token')

    if 'Admin' not in decoded_token.get('roles', []):
        return unauthorized_response('Unauthorized: insufficient permissions')

    # Journeys tablosundan verileri al
    try:
        response = journeys_table.scan()  # Tüm verileri çek, filtreleme veya sorgulama yapılabilir
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({
                'statusCode': 500,
                'message': 'Internal server error during data retrieval'
            })
        }

# Test için event ve context örneklerini kullanabilirsiniz.
    
    # event = {
#     "version": "2.0",
#     "routeKey": "POST /login",
#     "rawPath": "/dev2/login",
#     "rawQueryString": "",
#     "headers": {
#         "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDc1NDA4fQ.QoYloda8ull1x4w-fKhKSI-KFXw1-6qGw8YsfaVk0zs",
#         "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br"
#     },
#     "requestContext": {
#         "accountId": "405996282404",
#         "apiId": "o11xc731wl"
#     },
#     "body": {
       
#     }
        
# }


# response = lambda_handler(event, None)

# print(response)

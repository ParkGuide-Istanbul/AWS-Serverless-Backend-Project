import json
import boto3
import jwt
import datetime
import hashlib
from botocore.exceptions import ClientError

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# JWT için gizli anahtar (güvenli bir şekilde saklanmalı)
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'

def lambda_handler(event, context):
    # Kullanıcı adı ve şifresi API Gateway'den alınır
    
    body =  json.loads(event['body'])                   #event['body']  
    username = body['username']
    password = body['password']
    required_roles = body['requiredRoles']

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Kullanıcı bilgilerini DynamoDB'den kontrol et
    try:
        response = table.get_item(Key={'Username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return  {
                'statusCode': 500,
                'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal serer error: User not found'
                })
            }

    

    # Kullanıcı bulunursa ve şifre doğruysa JWT oluştur
    if 'Item' in response and response['Item']['Password'] == hashed_password:
        if response['Item']['IsVerified'] == "0":
            return {
                'statusCode': 501,
                'body': json.dumps({
                    'statusCode': 501,
                    'message': 'User not verified'
                })
            }
        
        user_roles = response['Item']['Roles']
        # İstenen rollerden en az biri kullanıcının rolleri arasında var mı kontrol et
        if not any(role in user_roles for role in required_roles):
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'statusCode': 403,
                    'message': 'You do not have the required permissions'
                })
            }
        
        # Token içeriği
        payload = {
            'username': username,
            'roles': list(response['Item']['Roles']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        # JWT oluştur
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print("token: " + token)
        print("\n")
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print("Decoded JWT Payload:")
        print(decoded_payload)
        return {
            'statusCode': 200,
            'body': json.dumps({
                    'statusCode': 200,
                    'message': {
                        'token': token,
                        'username': response['Item']['Username'],
                        'name': response['Item'].get('Name', 'Not Available'),  # Eğer Name yoksa
                        'surname': response['Item'].get('Surname', 'Not Available'),  # Eğer Surname yoksa
                        'roles': list(response['Item']['Roles']),
                        'IsInJourney': response['Item'].get('IsInJourney', '0'),  # Eğer IsInJourney yoksa
                    }
                })
            
        }
    else:
        return {
            'statusCode': 402,
            'body': json.dumps({
                    'statusCode': 402,
                    'message': 'Wrong password'
                })   
        }

# Test için
# event = {
#     "version": "2.0",
#     "routeKey": "POST /login",
#     "rawPath": "/dev2/login",
#     "rawQueryString": "",
#     "headers": {
#         "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br",
#         "content-length": "83",
#         "content-type": "application/json",
#         "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
#         "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
#         "user-agent": "PostmanRuntime/7.32.3",
#         "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
#         "x-forwarded-for": "78.180.71.41",
#         "x-forwarded-port": "443",
#         "x-forwarded-proto": "https"
#     },
#     "requestContext": {
#         "accountId": "405996282404",
#         "apiId": "o11xc731wl",
#         "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
#         "domainPrefix": "o11xc731wl",
#         "http": {
#             "method": "POST",
#             "path": "/dev2/login",
#             "protocol": "HTTP/1.1",
#             "sourceIp": "78.180.71.41",
#             "userAgent": "PostmanRuntime/7.32.3"
#         },
#         "requestId": "O_nxaiSCFiAEJLw=",
#         "routeKey": "POST /login",
#         "stage": "dev2",
#         "time": "26/Nov/2023:06:59:33 +0000",
#         "timeEpoch": 1700981973556
#     },
#     "body":   {
#         "username": "alpbeydemir",
#         "password": "blabla",
#         "requiredRoles": ["Admin", "ParkingSystemAdmin"] 
#     }  
    
    
# }
# lambda_handler(event, None)
import json
import boto3
import jwt
from botocore.exceptions import ClientError
from datetime import datetime
import random

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
reports_table = dynamodb.Table('Reports')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # Bu kısmı güvenli bir şekilde saklamalısınız

def generate_unique_report_id():
    while True:
        # 5 haneli rastgele bir sayı üret
        report_id = random.randint(10000, 99999)
        try:
            # Üretilen ID ile DynamoDB'de sorgulama yap
            response = reports_table.get_item(Key={'ReportId': str(report_id)})
            # Eğer bu ID'ye sahip bir kayıt yoksa, bu ID'yi dön
            if 'Item' not in response:
                return report_id
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise

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

    # Roller kontrolü (Rol isimlerini kendi gereksinimlerinize göre ayarlayın)
    roles = decoded_token.get('roles', [])
    if 'StandardUser' not in roles and 'User' not in roles:
        return unauthorized_response('Unauthorized: insufficient permissions')

    # Request body'den rapor bilgilerini al
    try:
        body = json.loads(event['body'])         #event['body']
        report_content = body['Content']
        report_topic = body['ReportTopic']
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request format'})
        }

    # Kullanıcı adını token'dan al
    user_name = decoded_token.get('username')
    if user_name is None:
        return unauthorized_response('User name not found in token')

    current_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


    # Raporu DynamoDB'ye kaydet
    try:
        report_id  = generate_unique_report_id()
        response = reports_table.put_item(
            Item={
                'ReportId': str(report_id),
                'Content': report_content,
                'Date': current_datetime,
                'ReportTopic': report_topic,
                'UserName': user_name
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error saving report'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Report saved successfully'})
    }

def unauthorized_response(message):
    return {
        'statusCode': 401,
        'body': json.dumps({'message': message})
    }



# event = {
#     "version": "2.0",
#     "routeKey": "POST /login",
#     "rawPath": "/dev2/login",
#     "rawQueryString": "",
#     "headers": {
#         "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiQWRtaW4iLCJTdGFuZGFydFVzZXIiXSwiZXhwIjoxNzAzNDE3NzUyfQ.GTGqs8uJQN8Yrr28cG0eY3RCx91ZMNN2yxZ-HOu90dc",
#         "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br"
#     },
#     "requestContext": {
#         "accountId": "405996282404",
#         "apiId": "o11xc731wl"
#     },
#     "body": {
#               "Content": "tefgdfgdfgst",
#               "ReportTopic": "tedfgdfgdfggst"

    
        
#     }
        
# }


# response = lambda_handler(event, None)

# print(response)

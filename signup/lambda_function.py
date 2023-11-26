import json
import boto3
import random
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Kullanıcı bilgilerini al

    body1 = json.loads(event['body'])
    body = json.loads(body1['body'])
    username = body['username']
    password = body['password']
    email = body['email']

    # E-posta adresini kontrol et
    try:
        email_response = table.scan(
            FilterExpression=Attr('Mail').eq(email)
        )
        if email_response['Items']:
            # E-posta adresi zaten kullanımda
            return {'statusCode': 400, 'body': json.dumps('Email already in use')}
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': json.dumps('Internal server error during email check')}

    # Kullanıcı adını kontrol et
    try:
        username_response = table.scan(
            FilterExpression=Attr('Username').eq(username)
        )
        if username_response['Items']:
            # Kullanıcı adı zaten kullanımda
            return {'statusCode': 400, 'body': json.dumps('Username already in use')}
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': json.dumps('Internal server error during username check')}

    # Yeni kullanıcıyı kaydet
    try:
        code = str(random.randint(100000, 999999))
        response = table.put_item(
            Item={
                'Username': username,
                'Password': password,
                'Mail': email,
                'IsVerified': '0',
                'Roles': {"StandartUser"},
                'Code': code 
            }
        )
        return {'statusCode': 200, 'body': json.dumps('User created successfully')}
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': json.dumps('Internal server error during user creation')}

# Test için örnek event

event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "content-length": "83",
        "content-type": "application/json",
        "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
        "user-agent": "PostmanRuntime/7.32.3",
        "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
        "x-forwarded-for": "78.180.71.41",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl",
        "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "domainPrefix": "o11xc731wl",
        "http": {
            "method": "POST",
            "path": "/dev2/login",
            "protocol": "HTTP/1.1",
            "sourceIp": "78.180.71.41",
            "userAgent": "PostmanRuntime/7.32.3"
        },
        "requestId": "O_nxaiSCFiAEJLw=",
        "routeKey": "POST /login",
        "stage": "dev2",
        "time": "26/Nov/2023:06:59:33 +0000",
        "timeEpoch": 1700981973556
    },
    "body": "{\r\n  \"body\": \"{\\\"username\\\": \\\"yeni_kullanici\\\", \\\"password\\\": \\\"yeni_sifre\\\",\\\"email\\\": \\\"yeni_kullanici@mail.com\\\"}\"\r\n}"
}

lambda_handler(event, None)

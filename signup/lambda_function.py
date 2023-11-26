import json
import boto3
import random
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# DynamoDB ayarları
ses_client = boto3.client('ses', region_name='eu-central-1')  
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def send_email(email, code):
    try:
        response = ses_client.send_email(
            Source='ParkGuideIstanbul@outlook.com.tr',  # E-posta gönderen adres
            Destination={
                'ToAddresses': [
                    email  # Alıcı e-posta adresi
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Your Verification Code'
                },
                'Body': {
                    'Text': {
                        'Data': f'Your verification code is: {code}'
                    }
                }
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

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
        # E-posta gönderimi
        email_response = send_email(email, code)
        if email_response:
            return {'statusCode': 200, 'body': json.dumps('User created and email sent successfully')}
        else:
            return {'statusCode': 500, 'body': json.dumps('User created but email sending failed')}
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
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": "{\r\n  \"body\": \"{\\\"username\\\": \\\"alpbeydemir\\\", \\\"password\\\": \\\"samplepassword\\\",\\\"email\\\": \\\"alpbeydemir@hotmail.com\\\"}\"\r\n}"
}

lambda_handler(event, None)

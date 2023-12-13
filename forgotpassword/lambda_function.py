import json
import boto3
import random
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# E-posta ve SMTP ayarları
sender_address = "ParkGuideIstanbul@outlook.com.tr"
passwordemail = "Parkguide123"

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # E-posta adresini al
    body = json.loads(event['body'])
    recipient_email = body['email']

    # Kullanıcı adını bul
    try:
        user_response = table.scan(
            FilterExpression=Attr('Mail').eq(recipient_email)
        )
        if not user_response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'statusCode': 404,
                    'message': 'User not found with that email'
                })
            }

        username = user_response['Items'][0]['Username']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
                'statusCode': 500,
                'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error during user search'
                })
            }

    # Sıfırlama kodunu oluştur
    try:
        code = str(random.randint(100000, 999999))
        # Burada kodu kullanıcının kaydında güncelleyebilirsiniz, örnek:


        table.update_item(
            Key={
                'Username': username
            },
            UpdateExpression="set Code = :c",
            ExpressionAttributeValues={
                ':c': code
            }
        )

        # E-posta gönderimi
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient_email
        message['Subject'] = 'Your Password Reset Code'
        body = f'Hello, \nyour username is : {username},\nYour password reset code is: {code}'
        message.attach(MIMEText(body, 'plain'))

        session = smtplib.SMTP('smtp-mail.outlook.com', 587)
        session.starttls()
        session.login(sender_address, passwordemail)
        text = message.as_string()
        session.sendmail(sender_address, recipient_email, text)
        session.quit()

        return {
                'statusCode': 200,
                'body': json.dumps({
                    'statusCode': 200,
                    'message': 'Password reset code sent successfully',
                    'username': username,
                    'email': recipient_email
                })
            }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
                'statusCode': 500,
                'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error during password reset process'
                })
            }


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
    "body": {
        "email": "alpbeydemir@hotmail.com"
    }
}

# lambda_handler(event, None)
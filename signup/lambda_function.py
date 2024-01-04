import json
import boto3
import random
import hashlib
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_address = "ParkGuideIstanbul@outlook.com.tr"
passwordemail = "Parkguide123"

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):
    # Kullanıcı bilgilerini al

    body =  json.loads(event['body'])          #event['body']                   

    username = body['username']

    password = body['password']
 
    recipient_email = body['email']
    name = body['name']  
    surname = body['surname']  

    hashed_password = hashlib.sha256(password.encode()).hexdigest()


    # E-posta adresini kontrol et
    try:
        email_response = table.scan(
            FilterExpression=Attr('Mail').eq(recipient_email)
        )
        if email_response['Items']:
            # E-posta adresi zaten kullanımda
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Email already in use'
                })   
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error during email check'
                })   
        }

    # Kullanıcı adını kontrol et
    try:
        username_response = table.scan(
            FilterExpression=Attr('Username').eq(username)
        )
        if username_response['Items']:
            # Kullanıcı adı zaten kullanımda
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Username already in use'
                })   
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error during username check'
                })   
        }

    # Yeni kullanıcıyı kaydet
    try:
        code = str(random.randint(100000, 999999))
        response = table.put_item(
            Item={
                'Username': username,
                'Password': hashed_password,
                'Mail': recipient_email,
                'Name': name,  
                'Surname': surname,  
                'IsVerified': '0',
                'Roles': ['StandardUser'] ,
                'Code': code,
                'IsInJourney': '0'
            }
        )

        # E-posta gönderimi
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = recipient_email
        message['Subject'] = 'Your Verification Code'
        body = f'Your verification code is: {code}'
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp-mail.outlook.com', 587) # use gmail with port
        session.starttls() # enable security
        session.login(sender_address, passwordemail) # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, recipient_email, text)
        session.quit()

        if email_response:
            return {
            'statusCode': 200,
            'body': json.dumps({
                    'statusCode': 200,
                    'message': 'User created and email sent successfully'
                })   
        }
        else:
            return {
            'statusCode': 500,
            'body': json.dumps({
                    'statusCode': 500,
                    'message': 'User created but email sending failed'
                })   
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error during user creation'
                })   
        }



# event = {
#     "version": "2.0",
#     "routeKey": "POST /login",
#     "rawPath": "/dev2/login",
#     "rawQueryString": "",
#     "headers": {
#         "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br"
#     },
#     "requestContext": {
#         "accountId": "405996282404",
#         "apiId": "o11xc731wl"
#     },
#     "body": {
#         "username": "alpbeydemir2",
#         "password": "samplepassword2",
#         "email": "mahmutizel@hotmail.com",
#         "name": "Mahmut",
#         "surname": "Izel"

#     }
    
# }

# lambda_handler(event, None)

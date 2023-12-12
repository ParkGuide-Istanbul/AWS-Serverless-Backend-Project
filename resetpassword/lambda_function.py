import json
import boto3
import hashlib
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Request body'den bilgileri al
    body = json.loads(event['body'])
    username = body['username']
    recipient_email = body['email']
    submitted_code = body['code']
    new_password = body['password']

    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    # Kullanıcıyı bul
    try:
        user_response = table.get_item(
            Key={'Username': username}
        )
        if 'Item' not in user_response:
            return {
            'statusCode': 404,
            'body': json.dumps({
                    'statusCode': 404,
                    'message': 'User not found'
                })   
        }

        user_info = user_response['Item']

        # Mail adresini kontrol et
        if user_info['Mail'] != recipient_email:
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Incorrect email for the given username'
                })   
        }

        # Kodu kontrol et
        if user_info['Code'] != submitted_code:
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Invalid code'
                })   
        }

        # Şifreyi güncelle
        table.update_item(
            Key={'Username': username},
            UpdateExpression="set Password = :p, Code = :c",
            ExpressionAttributeValues={
                ':p': hashed_password,
                ':c': '-'
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                    'statusCode': 200,
                    'message': 'Password reset successfully'
                })   
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'statusCode': 500,
                    'message': 'Internal server error'
                })   
        }


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
    "body": {
        "username": "alpbeydemir",
        "password": "samplepassword",
        "email": "alpbeydemir@hotmail.com",
        "code": "271296"
    }
}

lambda_handler(event, None)
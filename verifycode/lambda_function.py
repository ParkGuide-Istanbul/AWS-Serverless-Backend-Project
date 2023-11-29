import json
import boto3
from botocore.exceptions import ClientError

# DynamoDB ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Kullanıcıdan gelen bilgileri al
    body = event['body']
    username = body['username']
    password = body['password']
    code = body['code']

    # Kullanıcı bilgilerini DynamoDB'den kontrol et
    try:
        response = table.get_item(Key={'Username': username})
        if 'Item' not in response or response['Item']['Password'] != password:
            # Kullanıcı adı veya şifre yanlış
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Invalid username or password'
                })   
        }

        if response['Item']['Code'] == code:
            # Doğrulama kodu eşleşiyor, IsVerified'i güncelle
            table.update_item(
                Key={'Username': username},
                UpdateExpression='SET IsVerified = :val1, Code = :val2',
                ExpressionAttributeValues={':val1': '1', ':val2': '-'}
            )
            return {
            'statusCode': 200,
            'body': json.dumps({
                    'statusCode': 200,
                    'message': 'User verified successfully'
                })   
        }
        else:
            # Doğrulama kodu eşleşmiyor
            return {
            'statusCode': 400,
            'body': json.dumps({
                    'statusCode': 400,
                    'message': 'Invalid verification code'
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
        "password": "12345",
        "code": "402995"
    }
    
    
}

lambda_handler(event, None)
import json
import boto3
from botocore.exceptions import ClientError
import jwt

# Veritabanı ayarları
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'  # JWT için gizli anahtarınızı buraya girin

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
    token = header.get('authorization-token')  # 'Authorization' header'ını kontrol et

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

    # Roller kontrolü
    roles = decoded_token.get('roles', [])
    if 'Admin' not in roles:
        return unauthorized_response('Unauthorized: insufficient permissions')

    # Güncellenecek kullanıcı bilgilerini al
    try:
        request_body = json.loads(event['body'])     #event['body']
        users_to_update = request_body.get('editedUsers', [])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON format'})
        }

    # Kullanıcıları güncelle
    for user in users_to_update:
        username = user.get('Username')
        if not username:
            continue  # Kullanıcı adı yoksa bu kullanıcıyı atla

        # Update işlemleri için expression ve attribute_values hazırla
        update_expression = "SET "
        attribute_values = {}
        expression_attribute_names = {}
        for key, value in user.items():
            if key != 'Username':
                placeholder = f"#{key}"
                update_expression += f"{placeholder} = :{key}, "
                attribute_values[f":{key}"] = value
                expression_attribute_names[placeholder] = key
        update_expression = update_expression.rstrip(", ")

        try:
            table.update_item(
                Key={'Username': username},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            # Hata durumunda ilgili kullanıcı için mesajı kaydet
            user['update_status'] = 'Failed'

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Users updated successfully'})
    }


event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDc1NDA4fQ.QoYloda8ull1x4w-fKhKSI-KFXw1-6qGw8YsfaVk0zs",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
        "editedUsers": [
            {
                "Username": "alpbeydemir",
                "Name": "Alpp",
                "Surname": "Beydemir",
                "Mail": "alpbeydemir@hotmail.com",
                "Roles": ["Admin", "StandardUser","ParkingSystemAdmin"]
            },
            {
                "Username": "barisbeydemir",
                "Name": "bariss",
                "Surname": "Beydemir",
                "Mail": "beydemir18@itu.edu.tr",
                "Roles": ["Admin", "StandardUser","ParkingSystemAdmin"]
            }
        ]
    }
}


response = lambda_handler(event, None)

print(response)
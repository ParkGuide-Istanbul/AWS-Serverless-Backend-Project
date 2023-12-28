import json
import boto3
from botocore.exceptions import ClientError
import jwt

# Veritabanı ayarları
dynamodb = boto3.resource('dynamodb')
reports_table = dynamodb.Table('Reports')  # 'Reports' tablosunu tanımla

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

    # Reports tablosundan verileri al
    try:
        response = reports_table.scan()  # Tüm verileri çek, filtreleme veya sorgulama yapılabilir
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

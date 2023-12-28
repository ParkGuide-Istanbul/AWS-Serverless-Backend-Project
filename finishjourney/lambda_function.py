import boto3
import json
import jwt
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
journey_table = dynamodb.Table('Journeys')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'


def finish_active_journey(user):
    """Kullanıcının aktif yolculuğunu bitir."""
    response = journey_table.scan(
        FilterExpression='#usr = :user and IsFinished = :isFinished',
        ExpressionAttributeNames={
            '#usr': 'User'  # 'User' için takma ad
        },
        ExpressionAttributeValues={
            ':user': user,
            ':isFinished': '0'
        }
    )



    if 'Items' in response and len(response['Items']) > 0:
        active_journey = response['Items'][0]
        journey_table.update_item(
            Key={'JourneyId': active_journey['JourneyId']},
            UpdateExpression='SET IsFinished = :val',
            ExpressionAttributeValues={':val': '1'}
        )
        return True
    else:
        return False
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

    user = decoded_token.get('username')
    if not user:
        return unauthorized_response('User not found in token')

    if finish_active_journey(user):
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Journey finished successfully'})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No active journey to finish'})
        }

def unauthorized_response(message):
    return {
        'statusCode': 401,
        'body': json.dumps({'message': message})
    }


event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiQWRtaW4iLCJTdGFuZGFydFVzZXIiXSwiZXhwIjoxNzAzNDA0NTgzfQ.6VWgyEulr6oFuleeydx5mySuA5KrVKiTuEDaHxiYhuU",
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
           
    
        
    }
        
}


response = lambda_handler(event, None)

print(response)

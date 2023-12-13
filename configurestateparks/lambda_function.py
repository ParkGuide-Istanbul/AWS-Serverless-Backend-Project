import json
import boto3
import jwt
from botocore.exceptions import ClientError

# DynamoDB ve JWT ayarları
dynamodb = boto3.resource('dynamodb')
parks_table = dynamodb.Table('Parks')
SECRET_KEY = 'Q56WTH4D98N1J2D5Z6U1UTKLDI4J5D6F'

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

    # Roller kontrolü
    roles = decoded_token.get('roles', [])
    if 'Admin' not in roles and 'ParkingSystemAdmin' not in roles:
        return unauthorized_response('Unauthorized: insufficient permissions')

    # Request body'den park bilgilerini al
    try:
        body =  json.loads(event['body'])        #event['body']  
        park_updates = body['parks']
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request format'})
        }

    # Her park için state güncellemesi yap
    for park in park_updates:
        park_id = park.get('parkId')
        new_state = park.get('state')
        if park_id is None or new_state is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing parkId or state in request body'})
            }
        
        try:
            response = parks_table.update_item(
                Key={'id': str(park_id)},
                UpdateExpression='SET #state = :val',
                ExpressionAttributeNames={'#state': 'state'},
                ExpressionAttributeValues={':val': new_state},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {
                'statusCode': 500,
                'body': json.dumps({'message': f'Error updating park {park_id}'})
            }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Parks updated successfully'})
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
#         "authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDc1NDA4fQ.QoYloda8ull1x4w-fKhKSI-KFXw1-6qGw8YsfaVk0zs",
#         "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br"
#     },
#     "requestContext": {
#         "accountId": "405996282404",
#         "apiId": "o11xc731wl"
#     },
#     "body": {
#         "parks":[
#             {
#                 "parkId": "1168",
#                 "state": "0"
#             },
#             {
#                 "parkId": "2381",
#                 "state": "0"
#             }
#         ]
#     }
        
# }


# response = lambda_handler(event, None)

# print(response)
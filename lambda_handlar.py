import jwt
import json
import requests
import os



def lambda_handler(event, context):
    url = "https://api.ibb.gov.tr/ispark/ParkDetay?id=2381"
    response = requests.get(url)
    print(response.text)
    
    token = jwt.encode({'sub': username, 'exp': datetime.utcnow() + timedelta(hours=1)}, 'your-very-secret-key', algorithm='HS256')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    
    }




import json
import requests
import os



def lambda_handler(event, context):
    url = "https://www.google.com"
    response = requests.get(url)
    print(response.status_code)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



import json
import boto3
import requests


def lambda_handler(event, context):

    try:
        # İspark API'den veri al
        url = "https://api.ibb.gov.tr/ispark/Park"
        response = requests.get(url)

        if response.status_code != 200:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('Failed to retrieve data from İspark API')
            }

        parks_data = response.json()


        # DynamoDB'ye bağlan
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('Parks_cache')


        # API'den alınan verileri DynamoDB'ye ekle
        for park in parks_data:
            # Tüm verileri string'e dönüştür
            park_item = {k: str(v) for k, v in park.items()}

            # Veriyi DynamoDB'ye ekle
            table.put_item(Item=park_item)



        print(f"Total {len(parks_data)} parks updated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        

lambda_handler(None, None)
import requests
import boto3
from boto3.dynamodb.conditions import Key

# İspark API'sinden veri almak
def get_ispark_data():
    url = "https://api.ibb.gov.tr/ispark/Park"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Request Failed with status code {response.status_code}")

# DynamoDB'ye veri eklemek
def insert_to_dynamodb(data, table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    for item in data:
        table.put_item(
            Item={
                'id': str(item['parkID']),  # Direkt olarak değerleri ver
                'name': item['parkName'],
                'state': '1'  # String olarak '1' değerini ver
            }
        )
# Ana işlev
def main():
    ispark_data = get_ispark_data()
    print(f"İspark API'den çekilen park sayısı: {len(ispark_data)}")  # Park sayısını yazdır
    insert_to_dynamodb(ispark_data, 'Parks')

# Kodu çalıştırmak için main fonksiyonunu çağır
if __name__ == "__main__":
    main()

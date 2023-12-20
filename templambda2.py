import boto3

def get_unique_districts(table_name):
    # DynamoDB client'ını başlat
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Tüm öğeleri almak için scan yap
    response = table.scan()
    items = response['Items']

    # Benzersiz ilçeleri bir set içinde sakla
    unique_districts = set()
    for item in items:
        district = item['district']
        unique_districts.add(district)

    # Benzersiz ilçeleri ve sayılarını yazdır
    print("Unique Districts:", unique_districts)
    print("Total Number of Districts:", len(unique_districts))

# Fonksiyonu çağır
get_unique_districts('Parks_cache')

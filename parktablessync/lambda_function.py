import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    # Parks_cache ve Parks tablolarına bağlan
    parks_cache_table = dynamodb.Table('Parks_cache')
    parks_table = dynamodb.Table('Parks')

    # Parks_cache tablosundan tüm verileri al
    parks_cache_data = parks_cache_table.scan()['Items']

    # Parks tablosundan tüm verileri al
    parks_data = parks_table.scan()['Items']
    parks_data_dict = {item['id']: item for item in parks_data}

    for park_cache in parks_cache_data:
        park_id = park_cache['parkID']
        park_name = park_cache['parkName']

        # Eğer park ID, Parks tablosunda yoksa veya isim değişmişse
        if park_id not in parks_data_dict:
            # Eksik veya değişmiş parkı Parks tablosuna ekle
            parks_table.put_item(
                Item={
                    'id': park_id,
                    'name': park_name,
                    'state': '1'
                }
            )
        # Eğer isim değişmişse, eski kaydı sil
        if park_id in parks_data_dict and parks_data_dict[park_id]['name'] != park_name:
            parks_table.put_item(
                Item={
                    'id': park_id,
                    'name': park_name,
                    'state': parks_data_dict.get(park_id, {}).get('state', {'S': '1'})
                }
            )

    print('Parks tablosu güncellendi.')
lambda_handler(None, None)
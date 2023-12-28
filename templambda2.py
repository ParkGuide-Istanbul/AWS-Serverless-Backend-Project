import boto3


# DynamoDB'ye bağlantı
dynamodb = boto3.resource('dynamodb')

# Verilen string listesi
district_list =['ATAŞEHİR', 'KADIKÖY', 'ÜSKÜDAR', 'FATİH', 'KARTAL', 'BAŞAKŞEHİR', 'TUZLA', 'BEYOĞLU', 'KAĞITHANE', 'SULTANBEYLİ', 'GÜNGÖREN', 'SARIYER', 'AVCILAR', 'MALTEPE', 'BAKIRKÖY', 'ŞİŞLİ', 'BAYRAMPAŞA', 'ÇEKMEKÖY', 'ARNAVUTKÖY', 'ÜMRANİYE', 'BEYLİKDÜZÜ', 'GAZİOSMANPAŞA', 'KÜÇÜKÇEKMECE', 'EYÜP', 'BEYKOZ', 'ZEYTİNBURNU', 'PENDİK', 
'ÇATALCA', 'BÜYÜKÇEKMECE', 'BEŞİKTAŞ', 'BAĞCILAR', 'SİLİVRİ', 'ESENLER', 'SULTANGAZİ', 'BAHÇELİEVLER']

def check_districts(dynamodb, district_list):
    """
    DynamoDB'deki Districts tablosundan tüm item'ları alır ve verilen listeye göre kontrol eder.
    """
    table = dynamodb.Table('Districts')
    response = table.scan()
    items = response['Items']

    missing_districts = []

    for item in items:
        district_name = item['Name']
        adjacent_districts = [adj for adj in item['AdjacentDistricts']]

        if district_name not in district_list:
            missing_districts.append(district_name)

        for adj_district in adjacent_districts:
            if adj_district not in district_list:
                missing_districts.append(adj_district)

    return list(set(missing_districts))  # Benzersiz eksik ilçeleri döndür

# Eksik ilçeleri kontrol et
missing_districts = check_districts(dynamodb, district_list)
print(missing_districts)



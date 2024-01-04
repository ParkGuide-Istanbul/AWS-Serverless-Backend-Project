


import boto3
from botocore.exceptions import ClientError
import random
import datetime
import uuid

dynamodb_table_name = 'Journeys'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Kullanıcı adları ve lokasyonlar
usernames = ["alpbeydemir", "devrim24", "yeni_kullanici", "alpbeydemir2", "barisbeydemir"]
locations = [{"district": "ATAŞEHİR", "lat": "40.9847", "lng": "29.1067"},
{"district": "KADIKÖY", "lat": "40.9911", "lng": "29.0270"},
{"district": "ÜSKÜDAR", "lat": "41.0324", "lng": "29.0133"},
{"district": "FATİH", "lat": "41.0193", "lng": "28.9478"},
{"district": "KARTAL", "lat": "40.9023", "lng": "29.1920"},
{"district": "BAŞAKŞEHİR", "lat": "41.0978", "lng": "28.8062"},
{"district": "TUZLA", "lat": "40.8155", "lng": "29.3092"},
{"district": "BEYOĞLU", "lat": "41.0374", "lng": "28.9770"},
{"district": "KAĞITHANE", "lat": "41.0851", "lng": "28.9726"},
{"district": "SULTANBEYLİ", "lat": "40.9659", "lng": "29.2720"},
{"district": "GÜNGÖREN", "lat": "41.0225", "lng": "28.8721"},
{"district": "SARIYER", "lat": "41.1664", "lng": "29.0503"},
{"district": "AVCILAR", "lat": "40.9801", "lng": "28.7175"},
{"district": "MALTEPE", "lat": "40.9235", "lng": "29.1328"},
{"district": "BAKIRKÖY", "lat": "40.9833", "lng": "28.8675"},
{"district": "ŞİŞLİ", "lat": "41.0614", "lng": "28.9850"},
{"district": "BAYRAMPAŞA", "lat": "41.0357", "lng": "28.9126"},
{"district": "ÇEKMEKÖY", "lat": "41.0402", "lng": "29.1757"},
{"district": "ARNAVUTKÖY", "lat": "41.1842", "lng": "28.7407"},
{"district": "ÜMRANİYE", "lat": "41.0338", "lng": "29.0983"},
{"district": "BEYLİKDÜZÜ", "lat": "41.0015", "lng": "28.6415"},
{"district": "GAZİOSMANPAŞA", "lat": "41.0575", "lng": "28.9156"},
{"district": "KÜÇÜKÇEKMECE", "lat": "41.0214", "lng": "28.7731"},
{"district": "EYÜP", "lat": "41.0460", "lng": "28.9253"},
{"district": "BEYKOZ", "lat": "41.1236", "lng": "29.1083"},
{"district": "ZEYTİNBURNU", "lat": "40.9881", "lng": "28.9032"},
{"district": "PENDİK", "lat": "40.8766", "lng": "29.2334"},
{"district": "ÇATALCA", "lat": "41.1436", "lng": "28.4619"},
{"district": "BÜYÜKÇEKMECE", "lat": "41.0159", "lng": "28.5955"},
{"district": "BEŞİKTAŞ", "lat": "41.0422", "lng": "29.0077"},
{"district": "BAĞCILAR", "lat": "41.0341", "lng": "28.8330"},
{"district": "SİLİVRİ", "lat": "41.0734", "lng": "28.2465"},
{"district": "ESENLER", "lat": "41.0333", "lng": "28.8579"},
{"district": "SULTANGAZİ", "lat": "41.1092", "lng": "28.8826"},
{"district": "BAHÇELİEVLER", "lat": "40.9983", "lng": "28.8608"}
]

# Rasgele bir tarih ve gün üretme fonksiyonu
def random_date_and_day():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%dT%H:%M:%SZ'), random_date.strftime('%A')

# DynamoDB'ye uygun veri üretme
journey_data = []
for _ in range(100):  # 100 adet veri üret
    username = random.choice(usernames)
    start_location = random.choice(locations)
    end_location = random.choice(locations)
    journey_time, day_of_week = random_date_and_day()

    journey = {
        "JourneyId": str(uuid.uuid4()),
        "User": username,
        "StartingDistrict": start_location['district'],
        "StartingLocation(lat-lng)": f"{start_location['lat']}-{start_location['lng']}",
        "DestinationDistrict": end_location['district'],
        "DestinationLocation(lat-lng)": f"{end_location['lat']}-{end_location['lng']}",
        "StartTime": journey_time,
        "DayOfWeek": day_of_week,
        "IsFinished": "1"
    }
    journey_data.append(journey)

for journey in journey_data:
    try:
        response = table.put_item(Item=journey)
        print(f"Journey added: {journey['JourneyId']}")
    except ClientError as e:
        print(f"Error adding journey: {e.response['Error']['Message']}")


# Yazdırma veya veritabanına kaydetme
for data in journey_data:
    print(data)

# Not: Bu verileri DynamoDB'ye kaydetmek için uygun bir boto3 DynamoDB put_item() çağrısı eklemelisiniz.

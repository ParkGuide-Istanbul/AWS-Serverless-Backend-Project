

import boto3

# DynamoDB client oluştur
dynamodb = boto3.resource('dynamodb')

# 'Districts' tablosunu seç
table = dynamodb.Table('Districts')

# İlçe komşuluklarını içeren sözlük
district_adjacency = {
    "Arnavutköy": ["Başakşehir", "Esenler", "Eyüp", "Sultangazi"],
    "Avcılar": ["Büyükçekmece", "Esenyurt", "Küçükçekmece"],
    "Bağcılar": ["Bahçelievler", "Bakırköy", "Esenler", "Güngören", "Küçükçekmece"],
    "Bahçelievler": ["Bağcılar", "Bakırköy", "Güngören"],
    "Bakırköy": ["Bahçelievler", "Bağcılar", "Güngören", "Zeytinburnu"],
    "Başakşehir": ["Arnavutköy", "Avcılar", "Bağcılar", "Esenler", "Küçükçekmece", "Sultangazi"],
    "Bayrampaşa": ["Esenler", "Eyüp", "Gaziosmanpaşa", "Zeytinburnu"],
    "Beşiktaş": ["Beyoğlu", "Şişli"],
    "Beykoz": ["Çekmeköy", "Ümraniye", "Üsküdar"],
    "Beylikdüzü": ["Avcılar", "Büyükçekmece", "Esenyurt"],
    "Beyoğlu": ["Beşiktaş", "Eyüp", "Kâğıthane", "Şişli"],
    "Büyükçekmece": ["Avcılar", "Beylikdüzü", "Çatalca", "Esenyurt", "Silivri"],
    "Çatalca": ["Arnavutköy", "Büyükçekmece", "Silivri"],
    "Çekmeköy": ["Beykoz", "Sancaktepe", "Ümraniye"],
    "Esenler": ["Arnavutköy", "Bağcılar", "Başakşehir", "Bayrampaşa", "Gaziosmanpaşa", "Güngören"],
    "Esenyurt": ["Avcılar", "Beylikdüzü", "Büyükçekmece", "Küçükçekmece"],
    "Eyüp": ["Arnavutköy", "Bayrampaşa", "Beyoğlu", "Gaziosmanpaşa", "Sarıyer", "Sultangazi"],
    "Fatih": ["Beyoğlu", "Eyüp", "Gaziosmanpaşa", "Zeytinburnu"],
    "Gaziosmanpaşa": ["Bayrampaşa", "Eyüp", "Fatih", "Kâğıthane", "Sultangazi"],
    "Güngören": ["Bahçelievler", "Bakırköy", "Bağcılar", "Esenler", "Zeytinburnu"],
    "Kadıköy": ["Ataşehir", "Maltepe", "Ümraniye", "Üsküdar"],
    "Kâğıthane": ["Beşiktaş", "Beyoğlu", "Eyüp", "Şişli", "Sarıyer"],
    "Kartal": ["Maltepe", "Pendik", "Sancaktepe"],
    "Küçükçekmece": ["Avcılar", "Bağcılar", "Başakşehir", "Bakırköy", "Esenyurt", "Bahçelievler"],
    "Maltepe": ["Ataşehir", "Kadıköy", "Kartal", "Sancaktepe"],
    "Pendik": ["Kartal", "Sultanbeyli", "Tuzla"],
    "Sancaktepe": ["Ataşehir", "Çekmeköy", "Kartal", "Maltepe", "Sultanbeyli"],
    "Sarıyer": ["Beyoğlu", "Eyüp", "Kâğıthane"],
    "Silivri": ["Büyükçekmece", "Çatalca"],
    "Sultanbeyli": ["Pendik", "Sancaktepe", "Kartal"],
    "Sultangazi": ["Arnavutköy", "Başakşehir", "Eyüp", "Gaziosmanpaşa", "Sarıyer"],
    "Şile": ["Beykoz", "Çekmeköy", "Pendik"],
    "Şişli": ["Beşiktaş", "Beyoğlu","Kağıthane"],
    "Tuzla": ["Pendik"],
    "Ümraniye": ["Beykoz", "Çekmeköy", "Kadıköy", "Üsküdar", "Ataşehir", "Sancaktepe"],
    "Üsküdar": ["Beykoz", "Kadıköy", "Ümraniye", "Ataşehir"],
    "Zeytinburnu": ["Bakırköy", "Bayrampaşa", "Esenler", "Fatih", "Güngören", "Eyüp"],
    "Ataşehir": ["Kadıköy", "Maltepe", "Pendik", "Sancaktepe", "Ümraniye"]
}


# Her ilçe ve bitişik ilçeleri için DynamoDB'ye kayıt ekle
for district, neighbors in district_adjacency.items():
    response = table.put_item(
       Item={
            'Name': district.upper(),
            'AdjacentDistricts': [neighbor.upper() for neighbor in neighbors]
        }
    )
    print(f"{district} kaydedildi, Response: {response}")
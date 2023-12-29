import random
import hashlib
import boto3
from botocore.exceptions import ClientError

# Örnek isim ve soyisim listeleri
first_names = [
    "Ahmet", "Mehmet", "Mustafa", "Ayşe", "Fatma", "Elif", 
    "Emre", "Yusuf", "Merve", "Zeynep", "Kübra", "Ömer", 
    "Ali", "Cem", "Deniz", "Esra", "Gizem", "Hakan", 
    "İrem", "Kaan", "Lale", "Murat", "Nihal", "Onur", 
    "Pelin", "Rüya", "Selin", "Tolga", "Umut", "Volkan", 
    "Yeliz", "Zafer", "Aslı", "Burak", "Ceren", "Doruk", 
    "Ece", "Furkan", "Gözde", "Hande", "Işıl", "Koray", 
    "Leyla", "Mert", "Naz", "Oğuz", "Pınar", "Recep", 
    "Sena", "Tarık", "Ufuk", "Vildan", "Yasin", "Zehra"
]

last_names = [
    "Yılmaz", "Demir", "Kaya", "Şahin", "Çelik", "Aydın", 
    "Öztürk", "Arslan", "Doğan", "Altın", "Kara", "Güneş", 
    "Koç", "Güler", "Tekin", "Akar", "Çetin", "Kılıç", 
    "Aslan", "Çakır", "Can", "Türk", "Polat", "Yıldız", 
    "Kurt", "Erdoğan", "Özdemir", "Çetinkaya", "Şimşek", "Korkmaz", 
    "Sarı", "Uzun", "Özkan", "Taş", "Keskin", "Aksoy", 
    "Keser", "Demirci", "Özer", "Çoban", "Yıldırım", "Ateş", 
    "Yavuz", "Koçak", "Durmaz", "Özçelik", "Kaplan", "Çiftçi"
]

# Rol seçenekleri
roles = ["Admin", "StandardUser", "ParkingSystemAdmin"]

# Rastgele rol üretme fonksiyonu
def random_roles():
    return random.sample(roles, random.randint(1, len(roles)))

# Rastgele kullanıcı adı ve e-posta adresi üretme fonksiyonları
def random_username(first_name, last_name):
    return f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"

def random_email(first_name, last_name):
    domains = ["hotmail.com", "gmail.com", "outlook.com"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

# AWS ve DynamoDB yapılandırması
dynamodb_table_name = 'Users'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Kullanıcı verilerini üretme ve kaydetme
user_credentials = []
user_data = []

for _ in range(200):  # 200 adet kullanıcı üret
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    username = random_username(first_name, last_name)
    plain_password = random_username(last_name, first_name)  # Basit bir şifre
    hashed_password = hashlib.sha256(plain_password.encode()).hexdigest()

    user = {
        "Username": username,
        "Code": "-",
        "IsInJourney": "0",
        "IsVerified": "1",
        "Mail": random_email(first_name, last_name),
        "Name": first_name,
        "Password": hashed_password,
        "Roles": random_roles(),
        "Surname": last_name
    }

    # Kullanıcı bilgilerini kaydet
    try:
        table.put_item(Item=user)
    except ClientError as e:
        print(f"Error adding user: {e.response['Error']['Message']}")

    # Kullanıcı adı ve orijinal şifre kaydet
    user_credentials.append({'Username': username, 'Password': plain_password})
    user_data.append(user)

# İlk 5 kullanıcı bilgisini ve şifrelerini yazdır


print("\nUser Credentials:")
for credential in user_credentials:
    print(credential)

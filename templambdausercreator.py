import random
import hashlib
import boto3
from botocore.exceptions import ClientError

# Örnek isim ve soyisim listeleri
first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]

# Rol seçenekleri
roles = ["Admin", "StandardUser", "ParkingSystemAdmin"]

# Rastgele rol üretme fonksiyonu
def random_roles():
    return [{"S": role} for role in random.sample(roles, random.randint(1, len(roles)))]

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

for _ in range(100):  # 100 adet kullanıcı üret
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
        "Roles": {"S": random_roles()},
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
for credential in user_credentials[:5]:
    print(credential)

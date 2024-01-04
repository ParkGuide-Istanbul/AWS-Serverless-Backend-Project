import random
import datetime
import boto3
from botocore.exceptions import ClientError

dynamodb_table_name = 'Reports'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Kullanıcı adları listesi
usernames = [
    "volkandemirci33", "yusufuzun75", "mertuzun86", "onurdoğan27", 
    "mertşimşek20", "pınarçetinkaya33", "burakşimşek53", "gizemçetin82", 
    # ... (Diğer kullanıcı adlarınızı ekleyebilirsiniz)
]

# Rapor konuları ve içerikleri
report_topics = ["Sistem Hatası", "Kullanıcı Geri Bildirimi", "Performans Sorunu", "Güvenlik İhlali", "Yeni Özellik Önerisi"]
report_contents = ["Sistem beklenmedik bir hata verdi.", "Kullanıcı arayüzü iyileştirme önerisi.", "Performans yavaşlama sorunu.", "Potansiyel güvenlik açığı tespiti.", "Kullanıcı deneyimini artıracak yeni özellik teklifi.","Sistem beklenmedik bir hata verdi ve giriş yapamadım. Lütfen acil olarak kontrol edin.","Kullanıcı arayüzünde bazı butonlar çalışmıyor, düzeltilmesi gerekiyor.","Performans yavaşlama sorunu yaşıyorum, sayfalar çok geç açılıyor.","Potansiyel bir güvenlik açığı tespit ettim. Şifre sıfırlama işlemi güvenli değil gibi görünüyor.","Kullanıcı deneyimini artıracak yeni bir özellik teklif ediyorum: gece modu eklenmeli.","Park yerinde boş görünen bir yere gittim ancak yer doluydu. Bu durum düzeltilmeli.",
"Park sistemindeki harita güncellenmeli, bazı park yerleri haritada yanlış gözüküyor.",
"Mobil uygulamada bazı menüler çok karmaşık, daha basit bir arayüz tasarlanmalı.",
"Kullanıcı desteği yanıtları çok geç geliyor, bu konuda iyileştirme yapılmalı.",
"Park alanlarındaki sensörler bazen yanlış bilgi veriyor, teknik bir sorun olabilir.",
"Ödeme sistemi bazen hata veriyor ve kart bilgilerimi kabul etmiyor.",
"Park alanı rezervasyonum birden iptal oldu, sebebini anlayamadım.",
"Bir park yerine geldiğimde, yerin daha önceden başkası tarafından işgal edildiğini gördüm.",
"Park uygulaması bazen donuyor ve telefonumu yeniden başlatmak zorunda kalıyorum.",
"Uygulamadaki bildirimler çok fazla ve rahatsız edici, azaltılmalı ya da kullanıcı bu bildirimleri yönetebilmeli.",
"Park alanlarındaki sensörler bazen yanlış bilgi veriyor, teknik bir sorun olabilir.",
"Ödeme sistemi bazen hata veriyor ve kart bilgilerimi kabul etmiyor.",
"Park alanı rezervasyonum birden iptal oldu, sebebini anlayamadım.",
"Bir park yerine geldiğimde, yerin daha önceden başkası tarafından işgal edildiğini gördüm.",
"Park uygulaması bazen donuyor ve telefonumu yeniden başlatmak zorunda kalıyorum.",
"Uygulamadaki bildirimler çok fazla ve rahatsız edici, azaltılmalı ya da kullanıcı bu bildirimleri yönetebilmeli.",
"Park alanlarındaki sensörler bazen yanlış bilgi veriyor, teknik bir sorun olabilir.",
"Ödeme sistemi bazen hata veriyor ve kart bilgilerimi kabul etmiyor.",
"Park alanı rezervasyonum birden iptal oldu, sebebini anlayamadım.",
"Bir park yerine geldiğimde, yerin daha önceden başkası tarafından işgal edildiğini gördüm.",
"Park uygulaması bazen donuyor ve telefonumu yeniden başlatmak zorunda kalıyorum.",
"Uygulamadaki bildirimler çok fazla ve rahatsız edici, azaltılmalı ya da kullanıcı bu bildirimleri yönetebilmeli.",
"Park alanlarındaki sensörler bazen yanlış bilgi veriyor, teknik bir sorun olabilir.",
"Ödeme sistemi bazen hata veriyor ve kart bilgilerimi kabul etmiyor.",
"Park alanı rezervasyonum birden iptal oldu, sebebini anlayamadım.",
"Bir park yerine geldiğimde, yerin daha önceden başkası tarafından işgal edildiğini gördüm.",
"Park uygulaması bazen donuyor ve telefonumu yeniden başlatmak zorunda kalıyorum.",
"Uygulamadaki bildirimler çok fazla ve rahatsız edici, azaltılmalı ya da kullanıcı bu bildirimleri yönetebilmeli.",
"Park alanlarındaki sensörler bazen yanlış bilgi veriyor, teknik bir sorun olabilir.",
"Ödeme sistemi bazen hata veriyor ve kart bilgilerimi kabul etmiyor.",
"Park alanı rezervasyonum birden iptal oldu, sebebini anlayamadım.",
"Bir park yerine geldiğimde, yerin daha önceden başkası tarafından işgal edildiğini gördüm.",
"Park uygulaması bazen donuyor ve telefonumu yeniden başlatmak zorunda kalıyorum.",
"Uygulamadaki bildirimler çok fazla ve rahatsız edici, azaltılmalı ya da kullanıcı bu bildirimleri yönetebilmeli."
]

# Rastgele tarih üretme fonksiyonu
def random_date():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    return (start_date + datetime.timedelta(days=random_number_of_days)).strftime('%Y-%m-%dT%H:%M:%SZ')

# Benzersiz ReportId'ler üretme
report_ids = random.sample(range(10000, 99999), 200)

# Reports verilerini üretme
reports_data = []
for report_id in report_ids:
    report = {
        "ReportId": str(report_id),
        "Content": random.choice(report_contents),
        "Date": random_date(),
        "ReportTopic": random.choice(report_topics),
        "UserName": random.choice(usernames)
    }
    reports_data.append(report)

for report in reports_data:
    try:
        response = table.put_item(Item={
            'ReportId': report['ReportId'],
            'Content': report['Content'],
            'Date': report['Date'],
            'ReportTopic': report['ReportTopic'],
            'UserName': report['UserName']
        })
        print(f"Report added: ReportId {report['ReportId']}")
    except ClientError as e:
        print(f"Error adding report: {e.response['Error']['Message']}")







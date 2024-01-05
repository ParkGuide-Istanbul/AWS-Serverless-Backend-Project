# AWS-Serverless-Backend-Project
AWS Serverless Backend Project of ParkGuide İstanbul Application

## Routes: 




###**************************************************************************************

###/login   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/login  


post request


body sample:

```
{
    "username": "alpbeydemir",
    "password": "blabla",
    "requiredRoles": ["Admin", "ParkingSystemAdmin"] 
}
```
örnek dönüş değerleri şu şekilde:
```
{
    "statusCode": 200,
    "message": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldnJpbTI0Iiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAzNDIwMTUxfQ.HXDcLRJFM1_qGiYVD83EeQwJXifZS1eoN6q0vv67kl0",
        "username": "devrim24",
        "name": "Devrim",
        "surname": "Kafadar",
        "roles": [
            "StandardUser",
            "Admin"
        ],
        "IsInJourney": "0"
    }
}
```



###/signup   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/signup  


post request


```
{
    "username": "alpbeydemir",
    "password": "samplepassword",
    "email": "alpbeydemir@hotmail.com",
    "name": "Alp",
    "surname": "Beydemir"
}
```


###/verifycode   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/verifycode


post request


```
{
    "username": "alpbeydemir",
    "password": "12345",
    "code": "402995"
}
```

###/forgotpassword   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/forgotpassword


post request


```
{
    "email": "alpbeydemir@hotmail.com"
}
```

###/resetpassword  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/resetpassword


post request


```
{
    "username": "alpbeydemir",
    "password": "samplepassword",
    "email": "alpbeydemir@hotmail.com",
    "code": "271296"
}
```


### şifreler veritabanında hash lenmiş bir şekilde olduğu için şifreleri kaybetmemek adına şuanki kullanıcıları ve şifreleri aşağıya yazıyorum
```
alpbeydemir -> "password": "samplepassword",
devrim24 -> "password": "67890",
yeni_kullanici -> "password": "yeni_sifre",
barisbeydemir -> "password": "12345",
```

### bu aşamadan sonra yazılan btün endpointlerde headers a Authorization eklenmesi zorunludur

## örnek:

![Alt text](image.png)

## json formatında ise şu şekilde:

{
    "version": "2.0",

    "headers": {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDI4MTIzfQ.B7f7J-DPULjvJCZKdZv8hD3GIIhOnvF5xdb794TumLA",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl"
    },
    "body": {
        "username": "alpbeydemir",
        "password": "samplepassword",
        "code": "123456"
    }
        
}


###/listparks  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/listparks        ----> admin panel için

get request

## Authorization unutma

###/configurestateparks  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/configurestateparks       ----> admin panel için

post request



```
{
         "parks":[
             {
                 "parkId": "1168",
                 "state": "0"
             },
             {
                 "parkId": "2381",
                 "state": "1"
             }
         ]
}
```


###/getuserlist  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/getuserlist      ----> admin panel için

get request


###/edituserlist  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/edituserlist       ----> admin panel için

post request
```
{
    "editedUsers": [
        {
            "Username": "alpbeydemir",
            "Name": "Alpp",
            "Surname": "Beydemir",
            "Mail": "alpbeydemir@hotmail.com",
            "Roles": [
                "Admin",
                "StandardUser",
                "ParkingSystemAdmin"
            ]
        },
        {
            "Username": "barisbeydemir",
            "Name": "bariss",
            "Surname": "Beydemir",
            "Mail": "beydemir18@itu.edu.tr",
            "Roles": [
                "Admin",
                "StandardUser",
                "ParkingSystemAdmin"
            ]
        }
    ]
}
```



###/getnearestparks  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/getnearestparks       ----> mobil uygulama için

post request

```
{
        "district": "KADIKÖY", 
        "lat": "40.9911", 
        "lng": "29.0270"
        
}
```
en yakın müsait 10 park bilgeleri obje listesi olarak dönüyor


![Alt text](image-1.png)


###/startjourney  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/startjourney      ----> mobil uygulama için

post request

```
{
    "starting": {
        "startingdistrict": "KADIKÖY",
        "startinglat": "40.9911",
        "startinglng": "29.0270"
    },
    "destination": {
        "destinationdistrict": "SARIYER",
        "destinationlat": "40.9911",
        "destinationlng": "29.0270"
    }
}
```

o anki kendi konumunu "starting" in içine giriyor ilçe ile beraber, destination a da gitmek istediği lokasyonun konumunu ve ilçesini giriyor 


###/finishjourney ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/finishjourney     ----> mobil uygulama için

get request

o an aktive olan jourey sini bitiriyor, ya da iptal ediyor. İptal ve bitirme işlemi için aynı endpoint kullanılacak.


###/controljourney  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/controljourney     ----> mobil uygulama için

post request

```
{
    "district": "SARIYER",
    "lat": "41.1664",
    "lng": "29.0503"
}
```
kullanıcının o anki konumu post request ile gönderilir. kullanıcının journey destination ına yaklaşıp yaklaşmadığına göre cevap döner. Eğer yaklaşmışsa yakınındaki 10 müsait park yeri en yakın olandan en uzak olana doğru sıralanır.

bu endpoint notification için kullanılmak üzere tasarlandı. Kullanıcı uygulamadayken arkaplanda 5 dk kadar bir request atılır endpointe. Nezaman requestin reponse ında parklar listelenir ve status kosu 200 dönerse, kullanıcıya notification çıkartılır.


###/sendreport  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/sendreport     ----> mobil uygulama için

post request

```
{
    "Content": "sampletopic",
    "ReportTopic": "samplecontent"
}
```

kullanıcıların adminlere bir şeyi reportlayabilmesi için oluşturulmuş endpoint



###/getjourneys  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/getjourneys      ----> admin panel için

get request

bütün journey leri bilgileri ile beraber liste şeklinde veren endpoint, bunu liste halinde gösterirken backend in döndüğü journeyid yi kullanmayın kötü gözükür, onu js dosyası içinde variable lara atıp kendiniz id bastırıp gösterebilirsiniz.


###/getreports  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/getreports      ----> admin panel için

get request

Bütün raporlar bu endpoint ile listelenebiliyor, sadece Admin rolüne sahip kullanıcılar bu endpointe istek atabilir


###/getquicksearchresults  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/getquicksearchresults      ----> mobil uygulama için

get request

kullanıcının en sık gittiği 4 destinarion lat-lng-district




pip3 install pyjwt --target=.\getuserlist\ --no-user

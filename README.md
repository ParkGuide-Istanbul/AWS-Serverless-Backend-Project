# AWS-Serverless-Backend-Project
AWS Serverless Backend Project of ParkGuide İstanbul Application

## Routes: 

#**************************************************************MANUEL DEPLOYU UNUTMA*****************************************************************************

###******************************************************COK ONEMLI KENDIME NOT*****************************************************************************
aws console da lambda da test ederken -> event['body'] kullan
deploy ederken ->  json.loads(event['body'])  kullan
son aşamada json.loads kalsın
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

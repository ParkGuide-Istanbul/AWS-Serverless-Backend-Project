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

alpbeydemir -> "password": "samplepassword",
devrim24 -> "password": "67890",
yeni_kullanici -> "password": "yeni_sifre",
barisbeydemir -> "password": "12345",
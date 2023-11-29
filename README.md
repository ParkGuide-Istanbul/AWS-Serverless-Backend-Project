# AWS-Serverless-Backend-Project
AWS Serverless Backend Project of ParkGuide İstanbul Application

## Routes: 

#**************************************************************MANUEL DEPLOYU UNUTMA*****************************************************************************

###/login   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/login  


post request


body sample:

```
{
  "body": "{\"username\": \"alpbeydemir\", \"password\": \"samplepassword\"}"
}
```

###/signup   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/signup  


post request


```
{
    "body": "{\"username\": \"alpbeydemir\", \"password\": \"12345\", \"email\": \"alpbeydemir@hotmail.com\"}"
}
```


###/verifycode   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/verifycode


post request


```
{
    "body": "{\"username\": \"alpbeydemir\", \"password\": \"12345\", \"code\": \"402995\"}"
}
```

###/forgotpassword   ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/forgotpassword


post request


```
{
    "body": "{\"email\": \"alpbeydemir@hotmail.com\"}"
}
```

###/resetpassword  ->   https://o11xc731wl.execute-api.eu-central-1.amazonaws.com/dev2/resetpassword


post request


```
{
    "body": "{\"username\": \"alpbeydemir\", \"password\": \"blabla\", \"email\": \"alpbeydemir@hotmail.com\", \"code\": \"567912\"}"
}
```
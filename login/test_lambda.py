import pytest
import boto3
from lambda_function import lambda_handler  # Lambda fonksiyonunuzu buradan import edin
import json

def test_successful_login():
    event = {
        "version": "2.0",
        "routeKey": "POST /login",
        "rawPath": "/dev2/login",
        "rawQueryString": "",
        "headers": {
            "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "content-length": "83",
            "content-type": "application/json",
            "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
            "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
            "user-agent": "PostmanRuntime/7.32.3",
            "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
            "x-forwarded-for": "78.180.71.41",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "405996282404",
            "apiId": "o11xc731wl",
            "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
            "domainPrefix": "o11xc731wl",
            "http": {
                "method": "POST",
                "path": "/dev2/login",
                "protocol": "HTTP/1.1",
                "sourceIp": "78.180.71.41",
                "userAgent": "PostmanRuntime/7.32.3"
            },
            "requestId": "O_nxaiSCFiAEJLw=",
            "routeKey": "POST /login",
            "stage": "dev2",
            "time": "26/Nov/2023:06:59:33 +0000",
            "timeEpoch": 1700981973556
        },
        "body":   {
            "username": "selinkara11",
            "password": "karaselin33",
            "requiredRoles": ["Admin"] 
    }     
}
    
    # Lambda fonksiyonunu çağırın ve yanıtı test edin
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "doğru passaport test i başarısız"
    assert 'token' in json.loads(response['body'])['message'], "Token dönmedi"

    print("doğru passaport test i başarılı")


def test_wrong_password():
    event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "content-length": "83",
        "content-type": "application/json",
        "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
        "user-agent": "PostmanRuntime/7.32.3",
        "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
        "x-forwarded-for": "78.180.71.41",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl",
        "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "domainPrefix": "o11xc731wl",
        "http": {
            "method": "POST",
            "path": "/dev2/login",
            "protocol": "HTTP/1.1",
            "sourceIp": "78.180.71.41",
            "userAgent": "PostmanRuntime/7.32.3"
        },
        "requestId": "O_nxaiSCFiAEJLw=",
        "routeKey": "POST /login",
        "stage": "dev2",
        "time": "26/Nov/2023:06:59:33 +0000",
        "timeEpoch": 1700981973556
    },
    "body":   {
        "username": "devrim24",
        "password": "678905",
        "requiredRoles": ["StandardUser"] 
}     
}
            # Lambda fonksiyonunu çağırın ve yanıtı test edin
    response = lambda_handler(event, None)
    assert response['statusCode'] == 402, "yanlış passaport test i başarısız"
    

    print("yanlış passaport test i başarılı")
    

    

def test_user_not_found():
    event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "content-length": "83",
        "content-type": "application/json",
        "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
        "user-agent": "PostmanRuntime/7.32.3",
        "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
        "x-forwarded-for": "78.180.71.41",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl",
        "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "domainPrefix": "o11xc731wl",
        "http": {
            "method": "POST",
            "path": "/dev2/login",
            "protocol": "HTTP/1.1",
            "sourceIp": "78.180.71.41",
            "userAgent": "PostmanRuntime/7.32.3"
        },
        "requestId": "O_nxaiSCFiAEJLw=",
        "routeKey": "POST /login",
        "stage": "dev2",
        "time": "26/Nov/2023:06:59:33 +0000",
        "timeEpoch": 1700981973556
    },
    "body":   {
        "username": "devrim245",
        "password": "67890",
        "requiredRoles": ["StandardUser"] 
}     
}
            # Lambda fonksiyonunu çağırın ve yanıtı test edin
    response = lambda_handler(event, None)
    assert response['statusCode'] == 500, "olmayan kullanıcı test i başarısız"
   

    print("olmayan kullanıcı test i başarılı")
    


def test_user_not_verified():
    event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "content-length": "83",
        "content-type": "application/json",
        "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
        "user-agent": "PostmanRuntime/7.32.3",
        "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
        "x-forwarded-for": "78.180.71.41",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl",
        "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "domainPrefix": "o11xc731wl",
        "http": {
            "method": "POST",
            "path": "/dev2/login",
            "protocol": "HTTP/1.1",
            "sourceIp": "78.180.71.41",
            "userAgent": "PostmanRuntime/7.32.3"
        },
        "requestId": "O_nxaiSCFiAEJLw=",
        "routeKey": "POST /login",
        "stage": "dev2",
        "time": "26/Nov/2023:06:59:33 +0000",
        "timeEpoch": 1700981973556
    },
    "body":   {
        "username": "ahmetpolat61",
        "password": "polatahmet25",
        "requiredRoles": ["StandardUser"] 
}     
}
            # Lambda fonksiyonunu çağırın ve yanıtı test edin
    response = lambda_handler(event, None)
    assert response['statusCode'] == 501, "not verified test i başarısız"
    
    print("not verified test i başarılı")
    

def test_insufficient_permissions():
    event = {
    "version": "2.0",
    "routeKey": "POST /login",
    "rawPath": "/dev2/login",
    "rawQueryString": "",
    "headers": {
        "__requestverificationtoken": "3NAMpH5Gl6HAgNOKrfrWOuDcg0g3Z-2yZzscrBLJXEImvN0VY3zaRNVtMgVM5UMcIa3yTwJYiAaxES5BH6uX5Zl_UEzwBJtA5lYYx8RpVECnRdbMQaVDqHEuhPkir82aWn6c4A2",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "content-length": "83",
        "content-type": "application/json",
        "host": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "postman-token": "27036ed8-9f14-4d6c-a975-9d327cbf5915",
        "user-agent": "PostmanRuntime/7.32.3",
        "x-amzn-trace-id": "Root=1-6562ecd5-1db19ea53bf92fdc7acae38d",
        "x-forwarded-for": "78.180.71.41",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "405996282404",
        "apiId": "o11xc731wl",
        "domainName": "o11xc731wl.execute-api.eu-central-1.amazonaws.com",
        "domainPrefix": "o11xc731wl",
        "http": {
            "method": "POST",
            "path": "/dev2/login",
            "protocol": "HTTP/1.1",
            "sourceIp": "78.180.71.41",
            "userAgent": "PostmanRuntime/7.32.3"
        },
        "requestId": "O_nxaiSCFiAEJLw=",
        "routeKey": "POST /login",
        "stage": "dev2",
        "time": "26/Nov/2023:06:59:33 +0000",
        "timeEpoch": 1700981973556
    },
    "body":   {
        "username": "selinaksoy25",
        "password": "aksoyselin43",
        "requiredRoles": ["ParkingSystemAdmin"] 
}     
}
            # Lambda fonksiyonunu çağırın ve yanıtı test edin
    response = lambda_handler(event, None)
    assert response['statusCode'] == 403, "insufficient permission test i başarısız"
    
    print("insufficient permission test i başarılı")




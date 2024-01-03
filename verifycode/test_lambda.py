import pytest
import boto3
from lambda_function import lambda_handler  # Lambda fonksiyonunuzu buradan import edin
import json


def test_successful_verification():

    """dynamodb de belli bir kullanıcının( Username = kübraaslan44)  IsVerified attribute unu 1 yap ve Code attribute unu random6 ahneli bir sayı yap"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    table.update_item(
        Key={'Username': "kübraaslan44"},
        UpdateExpression='SET IsVerified = :val1, Code = :val2',
        ExpressionAttributeValues={':val1': '1', ':val2': '123456'}
    )

    event = {
        "body": json.dumps({
            "username": "kübraaslan44",
            "password": "aslankübra66",
            "code": "123456"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "Kullanıcı doğrulama testi başarısız"




def test_invalid_username_or_password():
    event = {
        "body": json.dumps({
            "username": "kübraaslan44",
            "password": "yanlisSifre",
            "code": "123456"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "Geçersiz kullanıcı adı veya şifre testi başarısız"

def test_invalid_verification_code():
    event = {
        "body": json.dumps({
            "username": "kübraaslan44",
            "password": "aslankübra66",
            "code": "yanlisKod"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "Geçersiz doğrulama kodu testi başarısız"







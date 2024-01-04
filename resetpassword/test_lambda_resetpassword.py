import pytest
import boto3
from lambda_function import lambda_handler  # Lambda fonksiyonunuzu buradan import edin
import json

def test_successful_password_reset():
    # DynamoDB'den doğrulama kodunu al
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.get_item(Key={'Username': "alpbeydemir2"})
    code = response['Item']['Code']

    # Şifre sıfırlama işlemini test et
    event = {
        "body": json.dumps({
            "username": "alpbeydemir2",
            "password": "yeniSifre",
            "email": "mahmutizel@hotmail.com",
            "code": code
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "Başarılı şifre sıfırlama testi başarısız"

    # Test sonrası kullanıcının Code özelliğini orijinal değerine geri döndür
    table.update_item(
        Key={'Username': "alpbeydemir2"},
        UpdateExpression="set Code = :c",
        ExpressionAttributeValues={
            ':c': code
        }
    )



def test_user_not_found():
    event = {
        "body": json.dumps({
            "username": "olmayanKullanici",
            "password": "sifre",
            "email": "email@example.com",
            "code": "123456"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404, "Kullanıcı bulunamadı testi başarısız"

def test_wrong_email():
    event = {
        "body": json.dumps({
            "username": "alpbeydemir2",
            "password": "sifre",
            "email": "yanlisemail@example.com",
            "code": "123456"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "Yanlış e-posta testi başarısız"

def test_invalid_code():
    event = {
        "body": json.dumps({
            "username": "alpbeydemir2",
            "password": "sifre",
            "email": "dogruemail@example.com",
            "code": "yanlisKod"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "Geçersiz kod testi başarısız"

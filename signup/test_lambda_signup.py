import pytest
import boto3
from lambda_function import lambda_handler  # Lambda fonksiyonunuzu buradan import edin
import json

def test_successful_signup():
    event = {
        "body": json.dumps({
            "username": "yeniKullanici1235678",
            "password": "GüvenliParola1!",
            "email": "fghfghfgh@hotmail.com",
            "name": "Yeni",
            "surname": "Kullanıcı"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "Başarılı kayıt testi başarısız"
    assert "User created and email sent successfully" in json.loads(response['body'])['message'], "Mesaj yanlış"

    """ı want to delete this item from mu Users table"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    delete_response = table.delete_item(
            Key={
                'Username': "yeniKullanici1235678"  # Bu öğeyi tanımlayan anahtar alan
            }
        )




def test_email_already_in_use():
    event = {
        "body": json.dumps({
            "username": "alpbeydemir",
            "password": "BaşkaParola2@",
            "email": "alpbeydemir@hotmail.com",
            "name": "alp",
            "surname": "beydemir"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "E-posta zaten kullanımda testi başarısız"
    assert "Email already in use" in json.loads(response['body'])['message'], "E-posta zaten kullanımda testi başarısız"

def test_username_already_in_use():
    event = {
        "body": json.dumps({
            "username": "alpbeydemir",
            "password": "YeniParola3#",
            "email": "alpbeydemir2@hotmail.com",
            "name": "Başka",
            "surname": "Kullanıcı"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "Kullanıcı adı zaten kullanımda testi başarısız"
    assert "Username already in use" in json.loads(response['body'])['message'], "Kullanıcı adı zaten kullanımda testi başarısız"







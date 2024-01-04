import json
import os
import sys
import pytest
from lambda_function import lambda_handler  # lambda_function modülünü import edin

# Mevcut dosyanın bir üst dizinine ve oradan login dizinine giden yol
relative_path = os.path.join(os.path.dirname(__file__), '..', 'login')
relative_path = os.path.join(relative_path, '..')

# Python'un modül yoluna bu yolu ekle
sys.path.append(os.path.abspath(relative_path))

# Şimdi modülü import edebilirsin
#from lambda_function import lambda_handler  # Mevcut dizindeki lambda fonksiyonu
from login.lambda_function import lambda_handler as login_lambda_handler  # login klasöründeki lambda fonksiyonu


# Bu, Lambda fonksiyonunun başarılı bir şekilde çalıştığını test eder
def test_lambda_handler_success():
    login_event = {
        "body":   {
            "username": "selinkara11",
            "password": "karaselin33",
            "requiredRoles": ["Admin"] 
        }  
    }   
    response_token = login_lambda_handler(login_event, None)
    response_token = json.loads(response_token['body'])['message']['token']
    event = {
        "headers": {"authorization-token": response_token}
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "getlistparks testi başarısız"


# Bu, geçersiz bir token durumunda hata döndürülüp döndürülmediğini test eder
def test_invalid_token():
    event = {
        "headers": {"authorization-token": "invalidToken"},
        "body": json.dumps({})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 401
    assert 'Invalid token' in json.loads(response['body'])['message']

# Bu, token sağlanmadığında hata döndürülüp döndürülmediğini test eder
def test_no_token_provided():
    event = {
        "headers": {},
        "body": json.dumps({})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 401
    assert 'No token provided' in json.loads(response['body'])['message']




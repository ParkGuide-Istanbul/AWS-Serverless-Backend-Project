import sys
import os
import pytest
import boto3
import json

# Mevcut dosyanın bir üst dizinine ve oradan login dizinine giden yol
relative_path = os.path.join(os.path.dirname(__file__), '..', 'login')
relative_path = os.path.join(relative_path, '..')

# Python'un modül yoluna bu yolu ekle
sys.path.append(os.path.abspath(relative_path))

# Şimdi modülü import edebilirsin
from lambda_function import lambda_handler  # Mevcut dizindeki lambda fonksiyonu
from login.lambda_function import lambda_handler as login_lambda_handler  # login klasöründeki lambda fonksiyonu
from startjourney.lambda_function import lambda_handler as startjourney_lambda_handler  # startjourney klasöründeki lambda fonksiyonu
from finishjourney.lambda_function import lambda_handler as finishjourney_lambda_handler  # finishjourney klasöründeki lambda fonksiyonu

# Test kodlarınızı burada yazabilirsiniz


def test_successful_get_nearest_parks():
    """önce login_handler ı kullanarak token ı al, sonra bu token ı kullanarak parkları güncelle"""
    login_event = {
        "body":   {
            "username": "aliçakır90",
            "password": "çakırali24",
            "requiredRoles": ["StandardUser"] 
        }  
    }   
    response_token = login_lambda_handler(login_event, None)
    response_token = json.loads(response_token['body'])['message']['token']

    event = {
        "headers": {"authorization-token": response_token},
        "body": json.dumps({
            "district": "SARIYER",
            "lat": "41.1664",
            "lng": "29.0503"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "yakın parkları listeleme testi başarısız"
    


def test_invalidjson():
    login_event = {
        "body":   {
            "username": "aliçakır90",
            "password": "çakırali24",
            "requiredRoles": ["StandardUser"] 
        }  
    }   
    response_token = login_lambda_handler(login_event, None)
    response_token = json.loads(response_token['body'])['message']['token']
    event = {
        "headers": {"authorization-token": response_token},
        "body": json.dumps({
                "district": "KADIKÖY",
                "lat": "40.9911"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400, "invalid json testi başarısız"








import sys
import os
import pytest
import boto3
import json
from boto3.dynamodb.conditions import Attr

# Mevcut dosyanın bir üst dizinine ve oradan login dizinine giden yol
relative_path = os.path.join(os.path.dirname(__file__), '..', 'login')
relative_path = os.path.join(relative_path, '..')

# Python'un modül yoluna bu yolu ekle
sys.path.append(os.path.abspath(relative_path))

# Şimdi modülü import edebilirsin
from lambda_function import lambda_handler  # Mevcut dizindeki lambda fonksiyonu
from login.lambda_function import lambda_handler as login_lambda_handler  # login klasöründeki lambda fonksiyonu


# Test kodlarınızı burada yazabilirsiniz


def test_successful_send_report():
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
            "Content": "test report",
            "ReportTopic": "test topic"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "rapor gönderme testi başarısız"


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Reports')


    response = table.scan(
        FilterExpression=Attr('Content').eq("test report")
    )

    if response['Items']:
        ReportId = response['Items'][0]['ReportId']

        
        table.delete_item(
            Key={'ReportId': ReportId}
        )





def test_no_token_provided():
    event = {
        "headers": {},
        "body": json.dumps({
            "Content": "test report",
            "ReportTopic": "test topic"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 401, "Token yoksa hata testi başarısız"
    assert "No token provided" in json.loads(response['body'])['message'], "Mesaj yanlış"

def test_invalid_token():
    event = {
        "headers": {"authorization-token": "gecersizToken"},
        "body": json.dumps({})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 401, "Geçersiz token testi başarısız"
    assert "Invalid token" in json.loads(response['body'])['message'], "Mesaj yanlış"

# Süresi dolmuş token ve yetersiz yetkilere sahip kullanıcı testleri benzer şekilde yapılabilir.

def test_expired_token_format():
    event = {
        "headers": {"authorization-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGJleWRlbWlyIiwicm9sZXMiOlsiU3RhbmRhcnRVc2VyIiwiQWRtaW4iXSwiZXhwIjoxNzAyNDc1NDA4fQ.QoYloda8ull1x4w-fKhKSI-KFXw1-6qGw8YsfaVk0zs"},
        "body": json.dumps({})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 401, "expired token testi başarısız"




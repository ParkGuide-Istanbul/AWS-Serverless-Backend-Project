import pytest
import boto3
from lambda_function import lambda_handler  # Lambda fonksiyonunuzu buradan import edin
import json
from boto3.dynamodb.conditions import Attr




def test_successful_code_sending():
    event = {
        "body": json.dumps({
            "email": "alpbeydemir@hotmail.com"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200, "Başarılı kod gönderimi testi başarısız"
    assert "Password reset code sent successfully" in json.loads(response['body'])['message'], "Mesaj yanlış"

    """dynamodb de Users tablosunda bu e maile sahip kullanıcının code attribute unu tekrar "-" yap"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Kullanıcının kullanıcı adını bul
    response = table.scan(
        FilterExpression=Attr('Mail').eq("alpbeydemir@hotmail.com")
    )

    if response['Items']:
        username = response['Items'][0]['Username']

        # Kullanıcıyı kullanıcı adına göre güncelle
        table.update_item(
            Key={'Username': username},
            UpdateExpression='SET Code = :val2',
            ExpressionAttributeValues={':val2': '-'}
        )




def test_user_not_found():
    event = {
        "body": json.dumps({
            "email": "bulunmayanemail@example.com"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404, "Kullanıcı bulunamadı testi başarısız"





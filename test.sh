if ! command -v python3 &> /dev/null
then
    echo "Python 3 yüklü değil. Yükleniyor..."
    brew install python@3.8
    brew link --overwrite python@3.8
else
    echo "Python 3 zaten yüklü."
fi

echo "pip güncelleniyor..."
python3 -m pip3 install --upgrade pip
echo "Bağımlılıklar requirements.txt'den yükleniyor..."
pip3 install -r requirements.txt

# AWS CLI kurulumu
echo "AWS CLI yükleniyor..."
brew install awscli
aws --version

# AWS kimlik bilgilerini ayarla
echo "AWS kimlik bilgileri ayarlanıyor..."
export AWS_ACCESS_KEY_ID=AKIAV5B2DUISHJQA22VA
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=eu-central-1



pytest .\configurestateparks\test_lambda_configurestateparks.py
pytest .\controljourney\test_lambda_controlljourney.py  
pytest .\edituserlist\test_lambda_edituser_list.py 
pytest .\finishjourney\test_lambda_finish_journey.py  
pytest .\forgotpassword\test_lambda_forgot_password.py 
pytest .\getjourneys\test_lambda_getjourneys.py  
pytest .\getnearestparks\test_lambda_getnearestparks.py  
pytest .\getquicksearchresults\test_lambda_getquicksearchresults.py
pytest .\getreports\test_lambda_getreports.py 
pytest .\getuserlist\test_lambda_getuserlist.py    
pytest .\listparks\test_lambda_list_parks.py 
pytest .\login\test_lambda_login.py 
pytest .\resetpassword\test_lambda_resetpassword.py  
pytest .\sendreports\test_lambda_sendreports.py  
pytest .\signup\test_lambda_signup.py   
pytest .\startjourney\test_lambda_startjourney.py  
pytest .\verifycode\test_lambda.py  


echo "AWS kimlik bilgileri siliniyor..."
export AWS_ACCESS_KEY_ID=sdfsd
export AWS_SECRET_ACCESS_KEY=sdfsdf
export AWS_DEFAULT_REGION=eu-west-1

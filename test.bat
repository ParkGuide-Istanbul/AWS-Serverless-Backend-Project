@echo off

:: Python sürümünü kontrol et
python --version 2>NUL | find "Python 3.8"
if %ERRORLEVEL% neq 0 (
    echo Python 3.8 bulunamadi. Lutfen manuel olarak yukleyin.
    exit /b
)

:: Python 3.8 bulunduysa, diğer komutlar çalıştırılabilir
echo Python 3.8 yuklu.

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

@echo off
echo Downloading AWS CLI...
powershell -Command "Invoke-WebRequest -Uri https://awscli.amazonaws.com/AWSCLIV2.msi -OutFile AWSCLIV2.msi"
echo Installing AWS CLI...
msiexec /i AWSCLIV2.msi /quiet /norestart
echo AWS CLI installed successfully.
aws --version

@echo off
SET AWS_ACCESS_KEY_ID=AKIAV5B2DUISHJQA22VA
SET AWS_SECRET_ACCESS_KEY=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
SET AWS_DEFAULT_REGION=eu-central-1

aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%
aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%
aws configure set default.region %AWS_DEFAULT_REGION%


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


@echo off
SET AWS_ACCESS_KEY_ID=sdfsdf
SET AWS_SECRET_ACCESS_KEY=sdfsdf
SET AWS_DEFAULT_REGION=eu-west-1

aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%
aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%
aws configure set default.region %AWS_DEFAULT_REGION%

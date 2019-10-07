# VOIP API Integration simulation

## Installation
```bash
git clone git@github.com:Addovej/voip-yad.git
cd voip-yad
```
To build:
```bash
docker-compose build
```
To apply migrations:
```bash
docker-compose run app flask db upgrade
```
To create a superuser:
```bash
docker-compose run app flask create-superuser exampl@email.com
```
To launch
```bash
docker-compose up -d
```
To test code style
```bash
docker-compose run app flake8 app/
```

### Not docker installation
```bash
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

### Configuration

Go to https://oauth.yandex.ru/ for registration a new OAuth app.

Then go to https://oauth.yandex.ru/authorize?response_type=token&display=popup&force_confirm=yes&client_id=client-id

Configure .env:

YA_DISK_APP_ID=your-app-id
YA_DISK_APP_SECRET=your-app-secret


## Requirements
Python 3.6+

## Keywords
Flask, API, Yandex.Disk, sqlalchemy, postgresql, flassger

# VOIP API Integration simulation

## Requirements
Python 3.7+

## Installation
```bash

```

### Configuration

Go to https://oauth.yandex.ru/ for registration a new OAuth app.

Then go to https://oauth.yandex.ru/authorize?response_type=token&display=popup&force_confirm=yes&client_id=<client-id>

Configure .env:

YA_DISK_APP_ID=YA_DISK_APP_ID
YA_DISK_APP_SECRET=YA_DISK_APP_SECRET
YA_DISC_TOKEN=YA_DISC_TOKEN

Token will be valid in next year.


To build:
```bash
docker-compose build
```
To apply migrations:
```bash
docker-compose run app flask db upgrade
```
to create a superuser:
```bash
docker-compose run app flask createsuperuser exampl@email.com
```


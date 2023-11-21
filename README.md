# QBotWebServices

A fast-api web service provided for qq bot

## Install

```
pip install -r requirements.txt
```

## Test

Create `.env` file under project root directory, and edit allowed urls like:

```
ALLOWED_URLS=["https://vip2.loli.io/", "https://smms.app/"]
```

You should use `--root-path` to indicate the api's root path.

```
uvicorn main:app --reload --root-path /qqbot
```

Access
1. `/redirect?url=<encoded_url>` to redirect to the url.
1. `/image?url=<encoded_image_url>` to reverse proxy an image.

## Deploy

TODO

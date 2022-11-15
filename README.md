# flat_rent_scraper
Collects flat rent proposals from different sites using parameters from the 'criteria.json' file. 

## 1. You should create a parameters file named 'criteria.json'.

The example:

{
  "price less or equal": 400,
  "rooms greate or equal": 1,
  "floor less or equal": 4,
  "square greate or equal": 40,
  "find any keyword": [
    "blok 5",
    "blok 6",
    "block 5",
    "block 6",
    "blocka 5",
    "blocka 6",
    "block v",
    "block vi",
  ]
}

## 2. Also, you should create a file 'private_info.json' with the data for Telegram:

The example:

{
  "bot_token": "87737627518:AAFmZjk98j76sghoVaCNSTPcvzQIsoy",
  "chat_id": "-10023487009"
}

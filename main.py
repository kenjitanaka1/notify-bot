import requests
import time
import json

# url to check
url = "https://www.sportsmans.com/shooting-gear-gun-supplies/modern-sporting-rifles/fn-scar-17s-308-winchester-162in-blackfde-semi-automatic-modern-sporting-rifle-201-rounds/p/1571047"
# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# telegram bot token file
with open('telegram_token.json') as f:
    token = json.load(f)['token']
# telegram api endpoint to send a message
out_url = f"https://api.telegram.org/bot{token}/sendMessage"
# id of the chat to send the message to. Hardcoded
chat_id = "-552787100"

# We'll start in the state assuming that the product was oos
was_oos = True

if __name__=='__main__':
    # download the homepage
    payload = {'chat_id': chat_id, 'text': f'Bot is now starting, checking: {url}'}
    requests.post(out_url, params=payload)

    while True:
        r = requests.get(url, headers=headers)

        http = r.content.decode()
        if not "\"btn btn-nostock\"" in http and was_oos:
            print("change detected, sending message to group.")
            payload = {'chat_id': chat_id, 'text': f'SCAR 17 now in stock: {url}'}
            requests.post(out_url, params=payload)
            was_oos=False
        elif "\"btn btn-nostock\"" in http and not was_oos:
            was_oos = True
        
        print("Waiting 60 seconds before retrying.")
        time.sleep(60)

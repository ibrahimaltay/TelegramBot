import requests
import json
import time
import secrets
import sys
from analyser.analyser import analyse_everything

id_map = {
    'bitcoin':'1',
    'ethereum': '1027',
    'terra-luna': '4172',
    'monero': '328',
    'stellar':'512',
    'bnb':'1839',
    'solana':'5426',
    'cardano':'2010',
    'xrp':'52',
    'polkadot-new':'6636',
    'avalance':'5805',
    'polygon':'3890',
    'algorand':'4030',
    'usd':'2781'
}

def generate_random_x_request_id():
    
    random_x_request_id_list = []
    random_x_request_id_list.append(secrets.token_hex(nbytes=4))
    random_x_request_id_list.append(secrets.token_hex(nbytes=2))
    random_x_request_id_list.append(secrets.token_hex(nbytes=2))
    random_x_request_id_list.append(secrets.token_hex(nbytes=2))
    random_x_request_id_list.append(secrets.token_hex(nbytes=6))
    random_x_request_id = "-".join(random_x_request_id_list)
    return random_x_request_id

def get_current_timestamp():
    return int(time.time())

def get_timestamp_from_n_days_ago(n=30):
    total_seconds = n*24*60*60
    return get_current_timestamp() - total_seconds

def get_historical_data_for_crypto(n_days, crypto, denominator='usd'):
    
    x_request_id = generate_random_x_request_id()

    headers = {
    'authority': 'api.coinmarketcap.com',
    'fvideo-id': '32a43e8bf61f9d1b847a066796283ab6ccb6f27b',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-platform': '"Linux"',
    'x-request-id': x_request_id,
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'origin': 'https://coinmarketcap.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://coinmarketcap.com/',
    'accept-language': 'en,en-US;q=0.9,tr-TR;q=0.8,tr;q=0.7',
}

    # I passed in n + 1 in the following method because it brings n amount of data this way.
    # If I pass in n, I get n-1 amount of data.

    start_time = str(get_timestamp_from_n_days_ago(n_days+1))
    end_time = str(get_current_timestamp())
    crypto_id = id_map[crypto]
    denominator_id = id_map[denominator]

    params = (
    ('id', crypto_id),
    ('convertId', denominator_id),
    ('timeStart', start_time),
    ('timeEnd', end_time),
)

    output = json.loads(requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical', headers=headers, params=params).content.decode('utf-8')) 
    # print(output)
    return output

def parse_historical_data_to_get_close_prices(content):
    close_prices: list = []
    for quote in content['data']['quotes']:
        close_price = quote['quote']['close']
        close_prices.append(int(close_price))
        # print(close_price)
    return close_prices

def analyse_crypto(param, time_span_days=365, moving_average_days=30, bollinger_bands_days=30):
    if param == 'help':
        print('analyse <crypto_name> <time_span_days> <moving_average_days> <bollinger_bands_days>')
        sys.exit()
    content = get_historical_data_for_crypto(time_span_days, param)
    parsed_content = parse_historical_data_to_get_close_prices(content)
    analyse_everything(parsed_content, moving_average_days, bollinger_bands_days)

if __name__ == '__main__':
    param = str(sys.argv[1])
    if param == 'help':
        print('analyse <crypto_name> <time_span_days> <moving_average_days> <bollinger_bands_days>')
        sys.exit()
    
    time_span_days = int(sys.argv[2])
    moving_average_days = int(sys.argv[3])
    bollinger_bands_days = int(sys.argv[4])

    content = get_historical_data_for_crypto(time_span_days, param)
    parsed_content = parse_historical_data_to_get_close_prices(content)
    analyse_everything(parsed_content, moving_average_days, bollinger_bands_days)


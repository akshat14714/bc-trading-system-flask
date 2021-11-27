import requests


def get_current_rate():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    exchange_rate = float(response.json()['bpi']['USD']['rate_float'])
    return exchange_rate

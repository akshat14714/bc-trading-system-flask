import config


def validate(user_bitcoin_balance, user_fiat_balance, user_level, form, exchange_rate):
    result = True
    btc_amount = float(form['bitcoin_amount'])
    type_of_trade = form['buysell']
    commission_type = form['commissiontype']
    btc_total = 0.0
    usd_total = 0.0

    total_usd_amount = btc_amount * exchange_rate
    commission = config.commission_rates[user_level] * total_usd_amount / 100

    if type_of_trade == 'buy':
        usd_total = btc_amount * exchange_rate
    else:
        btc_total = btc_amount

    if commission_type == 'usd':
        usd_total += commission
    else:
        btc_total += commission / exchange_rate

    if usd_total > user_fiat_balance:
        result = False

    if btc_total > user_bitcoin_balance:
        result = False

    return result

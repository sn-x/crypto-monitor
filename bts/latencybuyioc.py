from datetime import datetime
import websocket
import time
import json
import ssl


class BuyIOC:
    def __init__(self, bitstamp_endpoint, telegraf_client_init, currency_pair_init, trading_client_init):
        global telegraf_client
        global trading_client
        global currency_pair

        telegraf_client = telegraf_client_init
        trading_client = trading_client_init
        currency_pair = currency_pair_init

        marketdata_ws = websocket.WebSocketApp("wss://" + bitstamp_endpoint, on_open=on_open, on_message=on_message, on_error=on_error)
        marketdata_ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})


    def logtrade(data):
        price = data["data"]["price"]
        buy_ioc(price)
        time.sleep(1)
        fail_buy_ioc_insufficient_size(price)
        time.sleep(1)
        fail_buy_ioc_insufficient_balance(price)


def on_open(ws):
    try:
        subscribe_marketdata(ws)
    except Exception as e:
        print(e)


def subscribe_marketdata(ws):
    params = {
        'event': 'bts:subscribe',
        'data': {
            'channel': 'live_trades_' + currency_pair
        }
    }
    subscription = json.dumps(params)

    try:
        ws.send(subscription)
    except Exception as e:
        print(e)


def on_message(ws, data):
    data = json.loads(data)

    try:
        BuyIOC.logtrade(data)
    except Exception as e:
        print(e)

def on_error(ws, msg):
    print(msg)


def buy_ioc(price):
    adjusted_price = round(price - (price * 0.19), 2)
    amount         = 0.004
    base           = "btc"
    quote          = "usd"

    start_ts = int(time.time() * 1000000)

    try:
        response = trading_client.buy_limit_order(amount, adjusted_price, base, quote, None, True)
    except Exception as e:
        print(e)

    end_ts  = int(time.time() * 1000000)
    
    # 2020-02-23 11:39:48.254368
    exec_ts = int((datetime.strptime(response['datetime'], '%Y-%m-%d %H:%M:%S.%f').timestamp()) * 1000000)

    from_start_to_exec = exec_ts - start_ts
    from_exec_to_end = end_ts - exec_ts
    complete_run = end_ts - start_ts
    
    try:
        telegraf_client.metric('buyioc_' + currency_pair + "_duration", {'from_start_to_exec': from_start_to_exec, "from_exec_to_end": from_exec_to_end, "complete_run": complete_run}, tags={'exchange': 'bitstamp'})
    except Exception as e:
        print(e)


def fail_buy_ioc_insufficient_size(price):
    adjusted_price = round(price - (price * 0.19), 2)
    amount         = 0.000004
    base           = "btc"
    quote          = "usd"

    start_ts = int(time.time() * 1000000)

    try:
        response = trading_client.buy_limit_order(amount, adjusted_price, base, quote, None, True)
    except Exception as e:
        error = e

    end_ts  = int(time.time() * 1000000)

    complete_run = end_ts - start_ts

    try:
        telegraf_client.metric('fail_buyioc_' + currency_pair + "_duration", {"complete_run": complete_run}, tags={'exchange': 'bitstamp', 'reject_reason': 'insufficient_order_size'})
    except Exception as e:
        print(e)


def fail_buy_ioc_insufficient_balance(price):
    adjusted_price = round(price + (price * 0.19), 2)
    amount         = 40000
    base           = "btc"
    quote          = "usd"

    start_ts = int(time.time() * 1000000)

    try:
        response = trading_client.buy_limit_order(amount, adjusted_price, base, quote, None, True)
    except Exception as e:
        error = e

    end_ts  = int(time.time() * 1000000)

    complete_run = end_ts - start_ts

    try:
        telegraf_client.metric('fail_buyioc_' + currency_pair + "_duration", {"complete_run": complete_run}, tags={'exchange': 'bitstamp', 'reject_reason': 'insufficient_balance'})
    except Exception as e:
        print(e)

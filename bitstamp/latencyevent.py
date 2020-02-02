import websocket
import time
import json
import ssl


class Latency:
    def __init__(self, bitstamp_endpoint, telegraf_client_init, currency_pair_init):
        global telegraf_client
        global currency_pair
        telegraf_client = telegraf_client_init
        currency_pair = currency_pair_init

        marketdata_ws = websocket.WebSocketApp("wss://" + bitstamp_endpoint, on_open=on_open, on_message=on_message, on_error=on_error)
        marketdata_ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})


    def calcLatency(data):
        ws_ts   = int(data["data"]["microtimestamp"])
        ts      = int(time.time() * 1000000)
        latency = int(ts - ws_ts)

        try:
            telegraf_client.metric('event_latency_' + currency_pair, {"latency": latency}, tags={'exchange': 'bitstamp'})
        except Exception as e:
            print(e)          


def on_open(ws):
    try:
        subscribe_marketdata(ws)
    except Exception as e:
        print(e)


def subscribe_marketdata(ws):
    params = {
        'event': 'bts:subscribe',
        'data': {
            'channel': 'live_orders_' + currency_pair
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
        Latency.calcLatency(data)
    except Exception as e:
        print(e)
    

def on_error(ws, msg):
    print(msg)

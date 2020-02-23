import websocket
import json
import ssl


class OBSpread:
    def __init__(self, bitstamp_endpoint, telegraf_client_init, currency_pair_init):
        global telegraf_client
        global currency_pair
        telegraf_client = telegraf_client_init
        currency_pair = currency_pair_init

        marketdata_ws = websocket.WebSocketApp("wss://" + bitstamp_endpoint, on_open=on_open, on_message=on_message, on_error=on_error)
        marketdata_ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    def spread(data):
        highest_bid = data["data"]["bids"][0][0]
        lowest_ask  = data["data"]["asks"][0][0]

        try:
            telegraf_client.metric('ob_spread_' + currency_pair, {'highest_bid': highest_bid, 'lowest_ask': lowest_ask}, tags={'exchange': 'bitstamp'})
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
            'channel': 'order_book_' + currency_pair
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
        OBSpread.spread(data)
    except Exception as e:
        print(e)


def on_error(self, ws, msg):
    print(msg)
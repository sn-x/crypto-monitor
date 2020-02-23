from telegraf.client import TelegrafClient
from bts import latencybuyioc, latencytcp, latencyob, latencyevent, livetrades, obspread 
import bitstamp.client
import threading
import auth

bitstamp_ws_endpoint = "ws.bitstamp.net"
telegraf_client      = TelegrafClient(host="localhost", port=8094)
trading_client       = bitstamp.client.Trading(username=auth.username, key=auth.key, secret=auth.secret)

def buy_ioc_latency():
    while True:
        latencybuyioc.BuyIOC(bitstamp_ws_endpoint, telegraf_client, "btcusd", trading_client)


def orderbook_spread_btcusd():
    while True:
        obspread.OBSpread(bitstamp_ws_endpoint, telegraf_client, "btcusd")


def orderbook_latency_btcusd():
    while True:
        latencyob.Latency(bitstamp_ws_endpoint, telegraf_client, "btcusd")


def tcp_latency():
    while True:
        latencytcp.Latency(bitstamp_ws_endpoint, telegraf_client)


def event_latency_btcusd():
    while True:
        latencyevent.Latency(bitstamp_ws_endpoint, telegraf_client, "btcusd")


def live_trades_btcusd():
    while True:
        livetrades.Trades(bitstamp_ws_endpoint, telegraf_client, "btcusd")

buy_ioc_latency_thread   = threading.Thread(target=buy_ioc_latency)
orderbook_spread_thread  = threading.Thread(target=orderbook_spread_btcusd)
orderbook_latency_thread = threading.Thread(target=orderbook_latency_btcusd)
tcp_latency_thread       = threading.Thread(target=tcp_latency)
event_latency_thread     = threading.Thread(target=event_latency_btcusd)
live_trades_thread       = threading.Thread(target=live_trades_btcusd)

buy_ioc_latency_thread.start()
#orderbook_spread_thread.start()
#orderbook_latency_thread.start()
#tcp_latency_thread.start()
#event_latency_thread.start()
#live_trades_thread.start()


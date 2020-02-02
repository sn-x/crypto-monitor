from telegraf.client import TelegrafClient
from bitstamp import latencytcp, latencyob, latencyevent, livetrades, obspread 
import threading


bitstamp_endpoint = "ws.bitstamp.net"
telegraf_client   = TelegrafClient(host="localhost", port=8094)


def orderbook_spread_btcusd():
    while True:
        obspread.OBSpread(bitstamp_endpoint, telegraf_client, "btcusd")


def orderbook_latency_btcusd():
    while True:
        latencyob.Latency(bitstamp_endpoint, telegraf_client, "btcusd")


def tcp_latency():
    while True:
        latencytcp.Latency(bitstamp_endpoint, telegraf_client)


def event_latency_btcusd():
    while True:
        latencyevent.Latency(bitstamp_endpoint, telegraf_client, "btcusd")


def live_trades_btcusd():
    while True:
        livetrades.Trades(bitstamp_endpoint, telegraf_client, "btcusd")


orderbook_spread_thread  = threading.Thread(target=orderbook_spread_btcusd)
orderbook_latency_thread = threading.Thread(target=orderbook_latency_btcusd)
tcp_latency_thread       = threading.Thread(target=tcp_latency)
event_latency_thread     = threading.Thread(target=event_latency_btcusd)
live_trades_thread       = threading.Thread(target=live_trades_btcusd)


orderbook_spread_thread.start()
orderbook_latency_thread.start()
tcp_latency_thread.start()
event_latency_thread.start()
live_trades_thread.start()


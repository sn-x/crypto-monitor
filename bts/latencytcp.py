from tcp_latency import measure_latency
import time
import json
import ssl


class Latency:
    def __init__(self, bitstamp_endpoint, telegraf_client_init):
        self.telegraf_client = telegraf_client_init
        self.calcLatency(bitstamp_endpoint)

    def calcLatency(self, data):
        result = measure_latency(host=data, port=443, timeout=1)
        latency = result[0]

        try:
            self.telegraf_client.metric('tcp_latency', {"latency": latency}, tags={'exchange': 'bitstamp'})
        except Exception as e:
            print(e)
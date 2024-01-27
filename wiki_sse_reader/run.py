import httpx
from httpx_sse import connect_sse
import logging
import os
import pika
import time

URL = os.environ["URL"]
RABBIT_CONN_STR = os.environ["RABBIT_CONN_STR"]

def stream():
    """
    Run streaming
    """
    # TODO async loop?
    rabbit_conn = pika.connection.URLParameters(RABBIT_CONN_STR)
    with httpx.Client() as httpx_client, pika.BlockingConnection(rabbit_conn) as rabbit_client:
        httpx_connect_kwargs = {
            "client": httpx_client,
            "method": "GET",
            "url": URL,
            "headers": {"Accept": "application/json"}
        }
        channel = rabbit_client.channel()
        with connect_sse(**httpx_connect_kwargs) as event_source:
            for sse in event_source.iter_sse():
                # print(sse.event, sse.data, sse.id, sse.retry)
                logging.info("msg processed")
                channel.basic_publish(exchange="testqueue", routing_key="testqueue", body=sse.data)

if __name__ == '__main__':
    # TODO handle reconnect to continue from last event id?
    # https://github.com/florimondmanca/httpx-sse#handling-reconnections
    while True:
        try:
            stream()
        except:
            logging.warning("Connection break, repeat in 1s")
            time.sleep(1)

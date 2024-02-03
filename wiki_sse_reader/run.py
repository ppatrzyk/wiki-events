from datetime import datetime, timezone
import httpx
from httpx_sse import connect_sse
import json
import logging
import os
import pika
import time

URL = os.environ["URL"]
RABBIT_CONN_STR = os.environ["RABBIT_CONN_STR"]
RABBIT_EXCHANGE = os.environ["RABBIT_EXCHANGE"]

def _get_time():
    """
    Time format helper
    """
    return datetime.now(tz=timezone.utc).isoformat()

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
                msg = {
                    "created_at": _get_time(),
                    "data_raw_json": sse.data,
                }
                channel.basic_publish(exchange=RABBIT_EXCHANGE, routing_key=RABBIT_EXCHANGE, body=json.dumps(msg))
                logging.info("msg processed")

if __name__ == '__main__':
    # TODO handle reconnect to continue from last event id?
    # https://github.com/florimondmanca/httpx-sse#handling-reconnections
    while True:
        try:
            stream()
        except Exception as e:
            logging.warning("Connection break, repeat in 1s, error:")
            logging.warning(str(e))
            time.sleep(1)

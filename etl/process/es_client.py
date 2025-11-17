from time import sleep
import requests
import json
import os
from dotenv import load_dotenv
from utils import backoff

load_dotenv()

ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")

ES_URL = f"http://{ES_HOST}:{ES_PORT}"


@backoff(border_sleep_time=60, factor=3)
def test_es():
    r = requests.get(f"{ES_URL}")
    print(r.json(), flush=True)

from time import sleep
import requests
import json
import os
from dotenv import load_dotenv
from process.entities.models import FilmWorkESDoc, FilmWorkESDocRaw
from utils import backoff

schema = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english",
                },
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genres": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "description": {"type": "text", "analyzer": "ru_en"},
            "directors_names": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}

load_dotenv()

ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")

ES_URL = f"http://{ES_HOST}:{ES_PORT}"


@backoff(border_sleep_time=60, factor=1.5, start_sleep_time=10)
def test_es():
    r = requests.get(f"{ES_URL}")
    print(r.json(), flush=True)


@backoff(border_sleep_time=60, factor=1.5, start_sleep_time=10)
def create_scheme():
    headers = {"Content-Type": "application/json"}
    requests.put(f"{ES_URL}/movies", json=schema, headers=headers)


@backoff(border_sleep_time=60, factor=1.5, start_sleep_time=10)
def send_bulk(bulk: list[FilmWorkESDocRaw]):
    json.dumps(bulk)

    bulk_req_body = ""
    for fw in bulk:
        action = {"index": {"_index": "movies", "_id": fw.id}}
        bulk_req_body += json.dumps(action) + "\n"
        bulk_req_body += json.dumps(fw) + "\n"

    headers = {"Content-Type": "application/json"}

    r = requests.post(f"{ES_URL}/_bulk", data=bulk_req_body, headers=headers)

    print(r.status_code, r.text)

import time

import requests
import os
import json
# from Ingester import Ingester
# from Tunneler import Tunneler
from Ingester import Ingester
from testingTransformers import run, second_run, third_run
from tunnels.BinarySentimentalAnalysisTunnel import BinarySentimentalAnalysisTunnel


# from testingTransformers import run, second_run


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "(#GME OR GME OR Gamecorp) -is:retweet lang:en", "tag": "GME"},
        {"value": "(bitcoin OR #Bitcoin OR #btc) -is:retweet lang:eng", "tag": "Bitcoin"},
        {"value": "(Ethereum OR #Ethereum OR #ETH OR #eth) -is:retweet lang:eng", "tag": "Ethereum"},
        {"value": "(Tesla OR #Tesla OR #TSLA OR #tsla) -is:retweet lang:eng", "tag": "Tesla"},
        {"value": "(AstraZeneca OR #AstraZeneca) -is:retweet lang:eng", "tag": "AstraZeneca"},
        {"value": "(#Doge OR #Dogecoin OR #Dogecoins) -is:retweet lang:eng", "tag": "Dogecoin"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token, ingester):
    # Ensures we just try to reconnect if anything goes wrong
    while True:
        try:
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/stream?tweet.fields=entities,created_at", headers=headers, stream=True,
            )
            print(response.status_code)
            if response.status_code != 200:
                raise Exception(
                    "Cannot get stream (HTTP {}): {}".format(
                        response.status_code, response.text
                    )
                )
            for response_line in response.iter_lines():
                if response_line:
                    json_response = json.loads(response_line)
                    ingester.ingest(json_response)
                    print(json_response)
        except:
            print("Something went wrong")

def main():
    # third_run()
    # run()
    # second_run()
    BinarySentimentalAnalysisTunnel("tweets_nlp_ed")
    ingester = Ingester("tweets")

    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token, ingester)


if __name__ == "__main__":
    main()

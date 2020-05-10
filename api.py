import requests
import json

def get_parsed_body(url):
    return json.loads(requests.get(url).text)

def get_text(url):
    return requests.get(url).text
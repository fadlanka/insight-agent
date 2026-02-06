import requests

BASE_URL = "http://127.0.0.1:8000"

def post_daily_log(data: dict):
    resp = requests.post(f"{BASE_URL}/daily_logs", json=data)
    resp.raise_for_status()
    return resp.json()

def post_wishlist(data: dict):
    resp = requests.post(f"{BASE_URL}/wishlists", json=data)
    resp.raise_for_status()
    return resp.json()

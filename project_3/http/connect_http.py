# client.py
import requests

url = "https://baidu.com"

try:
    r = requests.get(url, timeout=5)
    print("Status:", r.status_code)
    print("Length:", len(r.content))
except Exception as e:
    print("Error:", e)co
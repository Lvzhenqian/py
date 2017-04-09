import requests
import json
import time

url = 'http://113.107.161.47:9966/graph/history'
head = {'Content-Type': 'application/json'}
end = int(time.time())
start = end - 60
data = {
    "start": start,
    "end": end,
    "cf": "AVERAGE",
    "endpoint_counters": [
        dict(endpoint="113.107.149.50", counter="cpu.irq"),
        dict(endpoint="113.107.149.50", counter="cpu.idle"),
        dict(endpoint="113.107.148.73", counter="cpu.idle")
    ]
}
r = requests.post(url, json.dumps(data))
g = r.json()
print(g)

import time,json

file= r'c:\windows\7roadyw\agent\cfg.json'
try:
    with open(file, mode='r', encoding='utf8') as f:
        cfg = json.loads(f.read())
    hostname,version = cfg['hostname'],cfg['version']
    metric = {
            "metric": "agent.version",
            "endpoint": hostname,
            "timestamp": int(time.time()),
            "step": 300,
            "value": version,
            "counterType": "GAUGE",
            "tags": ""
        }
except FileNotFoundError:
    metric = {}
except json.JSONDecodeError:
    metric = {}
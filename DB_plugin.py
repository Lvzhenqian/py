import json

config = r'c:\windows\7roadyw\agent\cfg.json'
date = r'c:\windows\7roadyw\agent\plugin\openfalcon_db_monitor.txt'
try:
	metric = []
	with open(config, mode='r', encoding='utf8') as f:
		cfg = json.loads(f.read())
	with open(date, mode='rt', encoding='utf8') as fd:
		for line in fd:
			mc, times, step, values, cType, tag = line.split('\t')
			OnceMeric = {
				"metric": mc,
				"endpoint": cfg['hostname'],
				"timestamp": int(times),
				"step": int(step),
				"value": float(values),
				"counterType": cType,
				"tags": tag
			}
			metric.append(OnceMeric)
except FileNotFoundError:
	metric = {}
except json.JSONDecodeError:
	metric = {}

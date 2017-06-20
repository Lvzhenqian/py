from poplib import POP3
import json


with open('./config.json') as f:
	conf = json.loads(f.read())



mail = POP3('mail.7road.com')
mail.user(conf['email']['name'])
mail.pass_(conf['email']['password'])
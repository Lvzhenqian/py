from flask import Flask, request, jsonify
from ..Client.TransClient import *

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
	return 'ok'


@app.route('/v1/push', methods=['POST'])
def Push_Metric_By_Youreself():
	rep = None
	logging.info('自定义数据上传接口')
	try:
		data = request.get_json()
		rep = UpdateMetric(data)
	except Exception as err:
		logging.error(err)
	if rep:
		logging.info('上传成功：{}'.format(rep))


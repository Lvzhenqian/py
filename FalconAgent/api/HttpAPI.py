from flask import Flask, request, jsonify
from Client import TransClient
from util.config import Geloger,DEBUG

app = Flask(__name__)
api_log = Geloger(name='api.HttpAPI', file='app.log', debug=DEBUG)


@app.route('/health', methods=['GET'])
def health():
    return jsonify('ok')


@app.route('/v1/push', methods=['POST'])
def Push_Metric_By_Youreself():
    rep = False
    api_log.info('自定义数据上传接口')
    try:
        data = request.get_json()
        rep = TransClient.UpdateMetric(data)
    except Exception as err:
        api_log.error(err)
        return jsonify('fail')
    if rep:
        api_log.info('上传成功：{}'.format(rep))
        return jsonify('successful')

from flask import Flask, render_template, request, jsonify, Response
import traceback
import json
from service.accident_severity_service import AccidentSeverityService
import os

app = Flask(__name__)
accident_severity_service = AccidentSeverityService()


@app.route('/', methods=["GET"])
def hello_world():
    return render_template('index.html')


@app.route('/predict', methods=["POST"])
def predict_severity():
    msg = {"msg": "Error while predicting severity"}
    try:
        input_data = dict(request.form)
        print("request: -> ", input_data)
        # status, res_data, msg = accident_severity_service.predict_accident_severity(input_data)
        res_data = accident_severity_service.predict_accident_severity(input_data)
        return Response(json.dumps(res_data), status=200, mimetype='application/json')
    except Exception:
        print(traceback.format_exc())
        return Response(json.dumps(msg), status=404, mimetype='application/json')


@app.route('/fetchlabels', methods=["GET"])
def fetch_labels():
    status = 404
    msg = "Error while fetching labels"
    try:
        res_data = {
            "label_data": accident_severity_service.fetch_labels()
        }
        return Response(json.dumps(res_data), status=200, mimetype='application/json')
    except Exception:
        print("fetchlabels: ", traceback.format_exc())
        return Response(json.dumps({"msg": msg}), status=404, mimetype='application/json')


@app.route('/fetchfeatures', methods=["GET"])
def fetch_features():
    status = 404
    msg = "Error while fetching features"
    try:
        res_data = {
            "features": accident_severity_service.fetch_features()
        }
        print(res_data)
        return Response(json.dumps(res_data), status=200, mimetype='application/json')
    except Exception:
        print("fetch features: ", traceback.format_exc())
        return Response(json.dumps({"msg": msg}), status=404, mimetype='application/json')


@app.route('/status', methods=["GET"])
def status():
    return jsonify({"status": "success"})


if __name__ == '__main__' or __name__ == 'app':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    print("server started: ", port)

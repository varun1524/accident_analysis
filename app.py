from flask import Flask, render_template, request, jsonify, Response
import traceback
import json
from service.accident_severity_service import AccidentSeverityService

app = Flask(__name__)
accident_severity_service = AccidentSeverityService()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/predict', methods=["POST"])
def predict_severity():
    status = 404
    res_data = {}
    msg = {"msg": "Error while predicting severity"}
    try:
        input_data = request.json
        status, res_data, msg = accident_severity_service.predict_accident_severity(input_data)
        return render_template("index.html", status=status, res_data=res_data, msg=msg)
    except Exception:
        print(traceback.format_exc())
        return render_template("index.html", status=status, res_data=res_data, msg=msg)


@app.route('/fetchlabels', methods=["GET"])
def fetch_labels():
    status = 404
    msg = "Error while fetching labels"
    try:
        res_data = {
            "label_data": accident_severity_service.fetch_labels()
        }
        print(res_data)
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


if __name__ == '__main__':
    # app.debug = True
    app.run()

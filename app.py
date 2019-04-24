from flask import Flask, render_template, request
import traceback

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


if __name__ == '__main__':
    app.run()

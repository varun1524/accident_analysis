from util.accident_analysis_pred import AccidentAnalysisPred


class AccidentSeverityService:
    def __init__(self):
        self.acc_analysis_pred = AccidentAnalysisPred()

    def validate_input(self):
        pass

    def preprocessing_input(self, input_data):
        return self.acc_analysis_pred.preprocess_data(input_data)

    def predict_accident_severity(self, input_data):
        input_data = self.acc_analysis_pred.preprocess_data(input_data)
        pred = self.acc_analysis_pred.predict(input_data)
        print("pred: ", pred)
        return pred

    def fetch_labels(self):
        return self.acc_analysis_pred.fetch_labels()

    def fetch_features(self):
        return self.acc_analysis_pred.features


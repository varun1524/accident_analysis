from util.accident_analysis_pred import AccidentAnalysisPred
import pandas as pd
from tabulate import tabulate


class AccidentSeverityService:
    def __init__(self):
        self.acc_analysis_pred = AccidentAnalysisPred()

    def validate_input(self):
        pass

    def preprocessing_input(self, input_data):
        input_dict = {}
        # input_data["Day_of_Week"] = int(input_data["Day_of_Week"])
        # input_data["Speed_limit"] = int(input_data["Speed_limit"])
        # input_data["Number_of_Vehicles"] = int(input_data["Number_of_Vehicles"])

        for key, value in input_data.items():
            input_dict[key] = [value]

        df = pd.DataFrame.from_dict(input_dict)
        df = self.acc_analysis_pred.preprocess_data(df)
        df = df[self.acc_analysis_pred.features]

        print("input_dict: ", input_dict)

        # df = pd.DataFrame.from_dict(input_dict)
        # df = df[self.acc_analysis_pred.features]

        print("input dataframe after preprocessing: ", df)
        # print(tabulate(df, headers='keys', tablefmt='psql'))

        return df

    def predict_accident_severity(self, input_data):
        input_data = self.preprocessing_input(input_data)

        # print("Before prediction:- ", input_data)
        # for key, value in
        input_data.to_csv("file_name.csv", sep='\t', encoding='utf-8')

        pred = self.acc_analysis_pred.predict(input_data)
        pred = self.acc_analysis_pred.class_dict[pred[0]]

        print("prediction ->  ", pred)
        return {"pred": pred}

    def fetch_labels(self):
        return self.acc_analysis_pred.fetch_labels()

    def fetch_features(self):
        return self.acc_analysis_pred.features


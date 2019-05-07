#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import re

#Visualisation Libraries
import matplotlib.pyplot as plt

#Training and Preprocessing Libraries
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score

# sampling
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE, ADASYN

# classifiers
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score

from sklearn.tree import export_graphviz
from subprocess import call
from IPython.display import Image


class AccidentAnalysisPred:

    def __init__(self):
        # class_dict = {'Fatal': 1, 'Severe': 2, 'Slight': 3}

        class_labels = ['Fatal', 'Severe', 'Slight']

        data1 = pd.read_csv("./data/accidents_2005_to_2007.csv")
        data2 = pd.read_csv("./data/accidents_2009_to_2011.csv")
        data3 = pd.read_csv("./data/accidents_2012_to_2014.csv")

        data = pd.concat([data1, data2, data3])

        drop_columns = ['Date', 'Accident_Index', 'Number_of_Casualties', 'Police_Force', 'Junction_Detail',
                        'Junction_Control', 'Special_Conditions_at_Site', 'Carriageway_Hazards',
                        'Did_Police_Officer_Attend_Scene_of_Accident', 'LSOA_of_Accident_Location',
                        'Local_Authority_(District)', 'Local_Authority_(Highway)']

        # pre processing
        data = self.preprocess_datetime(data)
        data1 = data.drop(drop_columns, axis=1, inplace=False)
        data1.dropna(inplace=True)
        # In[14]:

        # Encode "String" Labels into "Int" Labels for easy training
        self.le_Pedestrian_Crossing_Physical_Facilities = LabelEncoder()
        self.le_Light_Conditions = LabelEncoder()
        self.le_Weather_Conditions = LabelEncoder()
        self.le_Road_Surface_Conditions = LabelEncoder()
        self.le_Pedestrian_Crossing_Human_Control = LabelEncoder()
        self.le_Road_Type = LabelEncoder()

        self.le_Pedestrian_Crossing_Physical_Facilities.fit(data1["Pedestrian_Crossing-Physical_Facilities"])
        self.le_Light_Conditions.fit(data1["Light_Conditions"])
        self.le_Weather_Conditions.fit(data1["Weather_Conditions"])
        self.le_Road_Surface_Conditions.fit(data1["Road_Surface_Conditions"])
        self.le_Pedestrian_Crossing_Human_Control.fit(data1["Pedestrian_Crossing-Human_Control"])
        self.le_Road_Type.fit(data1["Road_Type"])

        data1 = self.preprocess_data(data1)

        train, test = train_test_split(data1, test_size=.20)

        # features = ["Longitude", "Latitude", "Number_of_Vehicles", "Day_of_Week", "Time", "Road_Type",
        #             "Speed_limit", "Pedestrian_Crossing-Human_Control", "Pedestrian_Crossing-Physical_Facilities",
        #             "Light_Conditions", "Weather_Conditions", "Road_Surface_Conditions", "Year", "day_of_year",
        #             "month", "Urban_or_Rural_Area"]

        features = ["Number_of_Vehicles", "Day_of_Week", "Time", "Road_Type", "Speed_limit",
                    "Pedestrian_Crossing-Human_Control", "Pedestrian_Crossing-Physical_Facilities",
                    "Light_Conditions", "Weather_Conditions", "Road_Surface_Conditions",
                    "month", "Urban_or_Rural_Area"]

        y_train = train['Accident_Severity']
        x_train = train[features]

        y_test = test['Accident_Severity']
        x_test = test[features]

        print(test.loc[:, x_train.columns != 'Accident_Severity'].head(0))

        print("x_train: ", x_train.shape)
        print("x_test: ", x_test.shape)
        print("y_train: ", y_train.shape)
        print("y_test: ", y_test.shape)

        self.clf = RandomForestClassifier(n_estimators=10)
        self.build_model(x_train, y_train)

        self.print_score(y_test, self.predict(x_test))

        # estimator = self.clf.estimators_[5]
        #
        # export_graphviz(estimator, out_file='./tree.dot',
        #                 feature_names=features,
        #                 class_names=class_labels,
        #                 rounded=True, proportion=False,
        #                 precision=2, filled=True)

    def convert_date_to_day_of_year(self, dt):
        result = re.findall(r'(\d{2})/(\d{2})/(\d{4})',dt)
        return result[0][0]

    def convert_date_to_month(self, dt):
        result = re.findall(r'(\d{2})/(\d{2})/(\d{4})',dt)
        return result[0][1]

    def preprocess_datetime(self, data):
        data['day_of_year'] = data.Date.apply(lambda x: self.convert_date_to_day_of_year(x))
        data['month'] = data.Date.apply(lambda x: self.convert_date_to_month(x))
        return data

    def preprocess_data(self, temp_data):
        temp_data = temp_data[temp_data.Weather_Conditions != 'Unknown']
        temp_data = temp_data[temp_data.Road_Type != 'Unknown']
        temp_data["Pedestrian_Crossing-Physical_Facilities"]= self.le_Pedestrian_Crossing_Physical_Facilities.transform(temp_data["Pedestrian_Crossing-Physical_Facilities"])
        temp_data["Light_Conditions"]= self.le_Light_Conditions.transform(temp_data["Light_Conditions"])
        temp_data["Weather_Conditions"] = self.le_Weather_Conditions.transform(temp_data["Weather_Conditions"])
        temp_data["Road_Surface_Conditions"] = self.le_Road_Surface_Conditions.transform(temp_data["Road_Surface_Conditions"])
        temp_data["Pedestrian_Crossing-Human_Control"] = self.le_Pedestrian_Crossing_Human_Control.transform(temp_data["Pedestrian_Crossing-Human_Control"])
        temp_data["Road_Type"] = self.le_Road_Type.transform(temp_data["Road_Type"])
        temp_data["Time"] = temp_data["Time"].astype(str)
        temp_data['Time'] = temp_data['Time'].str.slice(0, 2, 1)
        temp_data["Time"] = temp_data["Time"].astype(int)
        return temp_data

    def build_model(self, X_train, Y_train):
        print(self.clf)
        self.clf.fit(X_train, Y_train)

    def predict(self, X_test):
        pred = self.clf.predict(X_test)
        return pred

    def print_score(self, y_test, pred, average="macro"):
        acc = accuracy_score(y_test, pred)
        prec = precision_score(y_test, pred, average=average)
        recall = recall_score(y_test, pred, average=average)
        f2 = f1_score(y_test, pred, average=average)
        print("Accuracy Score: {}".format(acc))
        print("Precision Score: {}".format(prec))
        print("Recall Score: {}".format(recall))
        print("F1 Score: {}".format(f2))
        return acc, prec, recall, f2

    def fetch_labels(self):
        label_dict = {
            "Pedestrian_Crossing-Physical_Facilities": self.le_Pedestrian_Crossing_Physical_Facilities.classes_.tolist(),
            "Light_Conditions": self.le_Light_Conditions.classes_.tolist(),
            "Weather_Conditions": self.le_Weather_Conditions.classes_.tolist(),
            "Road_Surface_Conditions": self.le_Road_Surface_Conditions.classes_.tolist(),
            "Pedestrian_Crossing-Human_Control": self.le_Pedestrian_Crossing_Human_Control.classes_.tolist(),
            "Road_Type": self.le_Road_Type.classes_.tolist(),

        }

        features = ["Number_of_Vehicles", "Day_of_Week", "Time", "Road_Type", "Speed_limit",
                    "Pedestrian_Crossing-Human_Control", "Pedestrian_Crossing-Physical_Facilities",
                    "Light_Conditions", "Weather_Conditions", "Road_Surface_Conditions",
                    "month", "Urban_or_Rural_Area"]

        print("label_dict: ", label_dict)
        return label_dict








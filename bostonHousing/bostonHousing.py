# -*- coding: utf-8 -*-
"""
   Flask-RESTful API
"""
from flask import Flask, request, jsonify, render_template, request
from flask_restful import Resource, Api
from sklearn.externals import joblib
import pandas as pd 
import numpy as np
import os
import traceback


app = Flask(__name__)
api = Api(app)


mydir = os.getcwd()
filename = os.path.join(mydir, 'bostonHousing', 'static', 'model.pkl')

include = ['crime_rate', 'avg_number_of_rooms', 'distance_to_employment_centers', 'property_tax_rate', 'pupil_teacher_ratio']

model_columns = include
model = None
model = joblib.load(filename)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('crime_rate', 0, type=int)
    b = request.args.get('avg_number_of_rooms', 0, type=int)
    c = request.args.get('distance_to_employment_centers', 0, type=int)
    d = request.args.get('property_tax_rate', 0, type=int)
    e = request.args.get('pupil_teacher_ratio', 0, type=int)
    M = np.array([a, b, c, d, e])
    prediction = list(model.predict(M))
    err_down, err_up = pred_ints(model, M)
    return jsonify({'house_value': "%.2f" % prediction[0], 'stddev': err_down[0]})


def pred_ints(model, X, percentile=95):
    err_down = []
    err_up = []
    preds = []
    for pred in model.estimators_:
        preds.append(pred.predict(X)[0])
    err_down.append(np.percentile(preds, (100 - percentile) / 2. ))
    err_up.append(np.percentile(preds, 100 - (100 - percentile) / 2.))
    return err_down, err_up

@app.route('/predict', methods=['POST'])
def post():
    if model:
        try:
            json_ = request.get_json(force = True)
            query = pd.DataFrame(json_, index=[0])

            for col in model_columns:
                if col not in query.columns:
                    query[col] = 0

            df = query.values.reshape((-1, 5))

            prediction = list(model.predict(df))
            err_down, err_up = pred_ints(model, df)
            return jsonify({'down': err_down, 'prediction': "%.2f" % prediction[0], 'up': err_up})

        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        return 'no model here' 


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

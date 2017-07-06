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
    err_down, err_up, stddev = pred_ints(model, M)
    return jsonify({'low': "%.2f" % err_down[0], 'house_value': "%.2f" % prediction[0], 'up': "%.2f" % err_up[0], 'stddev': "%.2f" % stddev[0]})


def pred_ints(model, X, percentile=95):
    stddev = []
    err_down = []
    err_up = []
    preds = []
    for pred in model.estimators_:
        preds.append(pred.predict(X)[0])
    stddev.append(np.std(preds))
    err_down.append(np.percentile(preds, (100 - percentile) / 2. ))
    err_up.append(np.percentile(preds, 100 - (100 - percentile) / 2.))
    return err_down, err_up, stddev

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
            err_down, err_up, stddev = pred_ints(model, df)
            return jsonify({'lower limit': err_down[0], 'prediction': "%.2f" % prediction[0], 'upper limit': err_up[0], 'stddev': "%.2f" % stddev[0]})

        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        return 'no model here' 


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

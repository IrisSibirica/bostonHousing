# -*- coding: utf-8 -*-
"""
   Flask-RESTful API
"""

from flask import Flask, request, jsonify, render_template, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('crime_rate', 0, type=int)
    b = request.args.get('avg_number_of_rooms', 0, type=int)
    c = request.args.get('distance_to_employment_centers', 0, type=int)
    d = request.args.get('property_tax_rate', 0, type=int)
    e = request.args.get('pupil_teacher_ratio', 0, type=int)
    return jsonify(house_value=a + b + c + d + e, 
                   stddev = a)


@app.route('/predict', methods=['POST'])
def post():
    #if request.is_json:
        json_data = request.get_json(force = True)
        a = json_data['crime_rate']
        b = json_data['avg_number_of_rooms']
        c = json_data['distance_to_employment_centers']
        d = json_data['property_tax_rate']
        e = json_data['pupil_teacher_ratio']
        return jsonify(house_value=a + b + c + d + e,
                   stddev = a)
        #return jsonify(sum =  a + b)
    #else:
    #    return jsonify(status="Request was not JSON")


@app.route('/')
def index():
    return render_template('index.html')

#class Predict(Resource):
#api.add_resource(Predict, '/')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT))

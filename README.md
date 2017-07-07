# bostonHousing


Run: 

```
export FLASK_APP=bostonHousing
flask run
```

And you have a local Flask app at http://localhost:5000/

Or call:

```
 curl http://localhost:5000/predict -H application/json --data-binary '{ "crime_rate": 0.1,
  "avg_number_of_rooms": 4.0,
  "distance_to_employment_centers": 6.5,
  "property_tax_rate": 330.0,
  "pupil_teacher_ratio": 19.5
}'
```

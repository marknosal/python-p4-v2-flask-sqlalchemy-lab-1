# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    # earthquake = Earthquake.query.filter_by(id=id).first()

    # if earthquake:
    #     return make_response(earthquake.to_dict(), 200)
    # else:
    #     return make_response({'message': f'Earthquake {id} not found.'}, 404)
    # if earthquake:
    #     body = earthquake.to_dict()
    #     status = 200
    # else:
    #     body = {'message': f'Earthquake {id} not found.'}
    #     status = 404

    # return make_response(body, status)
    if earthquake := Earthquake.query.filter(Earthquake.id == id).first():
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    
    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    qualified_quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response_quakes = [quake.to_dict() for quake in qualified_quakes]
    body = {
        'count': len(response_quakes),
        'quakes': response_quakes
    }
    return make_response(body, 200)
    # qualified_quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    # response_quakes = []

    # for quake in qualified_quakes:
    #     new_quake = Earthquake(
    #         id = quake.id,
    #         location = quake.location,
    #         magnitude = quake.magnitude,
    #         year = quake.year
    #     )
    #     response_quakes.append(new_quake.to_dict())
        
    # response_body = {
    #     'count': len(qualified_quakes),
    #     'quakes': response_quakes
    # }

    # return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

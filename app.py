import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_restful import Resource, reqparse

#########################
## 1. create flask app: #
#########################

# 1.1 setup sqlite db
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'houseprices.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
Migrate(app, db)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mySecretKey'
api = Api(app)


##########################################
### 2. create a model from existing DB ###
##########################################

# MODELS
class HousePricesModel(db.Model):
    __table__ = db.Model.metadata.tables['HousePrices']
    __table_args__ = {'autoload': True}

    # Since I am using reflection I don't need a constructor. Define what to return.
    def json(self):
        return {'Id': self.Id, 'code': self.Code, 'price': self.price,
                'sold date': self.date, 'postcode': self.postcode, 'Property Type': self.propType,
                'New built?': self.newBuild, 'Estate Type': self.estateType, 'House/flat number': self.number,
                'Street Address': self.street, 'town': self.town, 'district': self.district, 'county': self.county}

    #################################################
    #### 3. perform CRUD to later move to crud.py ###
    #################################################


# RESOURCES
class Item(Resource):
    def get(self, Id):
        tw = HousePricesModel.query.filter_by(Id=Id).first()
        if tw:
            return tw.json()
        else:
            return {'Id': None}, 404


class ItemList(Resource):
    def get(self):
        return {'houses': list(map(lambda hp: hp.json(), HousePricesModel.query.all()))}
        return jsonify(hp.data)
        # or the one below/up:
        # houseprices = HousePricesModel.query.all()
        # return  [ hp.json() for hp in houseprices ]


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

        ####################
        #### 3. end CRUD ###
        ####################


# WE ARE NOT USING THIS ANYMORE SINCE WE ARE BUILDING THE API
# @app.route("/")
# def home():
# print("Data in rows:", HousePricesModel.query.count())
# hptowns = HousePricesModel.query.filter_by(district='ENFIELD').filter_by(price='5000000').all()
# all = HousePricesModel.query.all()
# count = HousePricesModel.query.count()
# return render_template("index.html", count=count, towns=hptowns, all=all)
# return render_template("index.html", towns=hptowns)

api.add_resource(HelloWorld, '/', '/hello')
api.add_resource(ItemList, '/houses')
api.add_resource(Item, '/item/<string:Id>')


if __name__ == '__main__':
    app.run(debug=True)

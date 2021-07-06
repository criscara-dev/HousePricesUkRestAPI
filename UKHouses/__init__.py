import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_rest_paginate import Pagination

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

# Possible configurations for Paginate
app.config['PAGINATE_PAGE_SIZE'] = 20
# app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
# app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
# app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
# app.config['PAGINATE_PAGINATION_OBJECT_KEY'] = "pagination"
app.config['PAGINATE_DATA_OBJECT_KEY'] = "houses"
pagination = Pagination(app, db)


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
                'sold date': self.date.isoformat(sep=' '), 'postcode': self.postcode, 'Property Type': self.propType,
                'New built?': self.newBuild, 'Estate Type': self.estateType, 'House/flat number': self.number,
                'Street Address': self.street, 'town': self.town, 'district': self.district, 'county': self.county}

    #################################################
    #### 3. perform CRUD to later move to crud.py ###
    #################################################


"""
Resource fields for marshalling
"""
page_fields = {
    'Id': fields.String, 'code': fields.String, 'price': fields.String, 'sold date': fields.String,
    'postcode': fields.String, 'Property Type': fields.String, 'New built?': fields.String,
    'Estate Type': fields.String, 'House/flat number': fields.String, 'Street Address': fields.String,
    'town': fields.String, 'district': fields.String, 'county': fields.String
}


# RESOURCES
class House(Resource):
    def get(self, Id):
        tw = HousePricesModel.query.filter_by(Id=Id).first()
        if tw:
            return tw.json()
        else:
            return {'Id': None}, 404


class HouseList(Resource):
    def get(self):
        houseprices = HousePricesModel.query.all()
        return pagination.paginate([hp.json() for hp in houseprices], page_fields)


class Home(Resource):
    def get(self):
        # return {'hello':'world'}
        return render_template('index.html'), 200

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

api.add_resource(HouseList, '/houses')
api.add_resource(House, '/house/<string:Id>')
api.add_resource(Home, '/', '/index')

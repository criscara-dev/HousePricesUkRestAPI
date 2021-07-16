import os
import sqlite3
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_rest_paginate import Pagination
from typing import Dict, List, Union

# 1.1 setup sqlite db
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "houseprices.db")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "houseprices.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
Migrate(app, db)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "mySecretKey"
api = Api(app)
ItemJSON = Dict[str, Union[int, str, float, bool]]


# Possible configurations for Paginate
app.config["PAGINATE_PAGE_SIZE"] = 20
# app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
# app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
# app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
# app.config['PAGINATE_PAGINATION_OBJECT_KEY'] = "pagination"
app.config["PAGINATE_DATA_OBJECT_KEY"] = "houses"
pagination = Pagination(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


# MODELS -  a helper that help us ti retrieve HousePricesModel objects from the db - internal repr of an Entity
class HousePricesModel(db.Model):
    __table__ = db.Model.metadata.tables["HousePrices"]
    __table_args__ = {"autoload": True}

    def json(self) -> ItemJSON:
        return {
            "Id": self.Id,
            "code": self.Code,
            "price": self.price,
            "date": self.date.isoformat(),
            "postcode": self.postcode,
            "Property Type": self.propType,
            "New built?": self.newBuild,
            "Estate Type": self.estateType,
            "House/flat number": self.number,
            "Street Address": self.street,
            "town": self.town,
            "district": self.district,
            "county": self.county,
        }

    @classmethod
    def find_all(cls) -> List["HousePricesModel"]:
        return cls.query.all()


"""
Resource fields for marshalling
"""
page_fields = {
    "Id": fields.String,
    "code": fields.String,
    "price": fields.String,
    "date": fields.String,
    "postcode": fields.String,
    "Property Type": fields.String,
    "New built?": fields.String,
    "Estate Type": fields.String,
    "House/flat number": fields.String,
    "Street Address": fields.String,
    "town": fields.String,
    "district": fields.String,
    "county": fields.String,
}


# RESOURCES - external repr of an Entity, it maps endpoints
class Home(Resource):
    @classmethod
    def get(cls):
        return render_template("index.html"), 200


class House(Resource):
    @classmethod
    def get(cls, Id):
        house_id = HousePricesModel.query.filter_by(Id=Id).first()
        if house_id:
            return house_id.json(), 200
        else:
            return {"Id": None}, 404


class HouseList(Resource):
    def get(self):
        args = request.args
        from_date = args.get("from")
        to_date = args.get("to")
        if (
            request.method == "GET"
            and "from" in args is not None
            and "to" in args is not None
        ):
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            query = (
                "SELECT * FROM HousePrices WHERE date BETWEEN ? AND ? ORDER BY date ASC"
            )
            result = cursor.execute(
                query,
                (
                    from_date,
                    to_date,
                ),
            )
            housesInDateRange = []

            def parse_house_record(row):
                return {
                    "Id": row[0],
                    "code": row[1],
                    "date": row[3],
                    "postcode": row[4],
                    "Property Type": row[5],
                    "New built?": row[6],
                    "Estate Type": row[7],
                    "House/flat number": row[8],
                    "Street Address": row[9],
                    "town": row[10],
                    "district": row[11],
                    "county": row[12],
                }

            for row in result:
                housesInDateRange.append(parse_house_record(row))
            connection.close()
            return pagination.paginate(housesInDateRange, page_fields)

        else:
            houseprices = HousePricesModel.find_all()
            return pagination.paginate([hp.json() for hp in houseprices], page_fields)


api.add_resource(Home, "/", "/index")
api.add_resource(HouseList, "/houses")
api.add_resource(House, "/house/<string:Id>")

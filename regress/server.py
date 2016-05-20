from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from regress.database import create_model, read_model
from regress.model import Model, model_to_svg


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("format")


class ModelAPI(Resource):
    def post(self):
        model = Model.from_dict(request.get_json())
        model.regress()
        create_model(model)
        return model.to_dict()

    def get(self):
        args = parser.parse_args()
        model = read_model(args.get("name"))
        if model:
            if args.get("format") == "svg":
                return model_to_svg(model)
            return model.to_dict()
        return {"msg": "Model {} not found".format(args.get("name"))}


api.add_resource(ModelAPI, "/model")

from flask_restful import Resource,reqparse,request
from flask import Response,send_file
from models.cities import CitiesModel
from models.state import StateModel
from models.countries import CountryModel
from models.image import ImageModel
from werkzeug.utils import secure_filename
import base64


class CityResource(Resource):

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'state_id',
            type=int,
            required=False
        )

        data = local.parse_args()

        if data['state_id']:
            return {'cities':[city.json() for city in CitiesModel.get_city_by_state(**data)]}

        return {'cities':[city.json() for city in CitiesModel.query.all()]}


class StateResource(Resource):


    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )

        data = local.parse_args()

        if data['id']:
            return {'states':[state.json() for state in StateModel.get_by_country(data['id'])]}

        return {'states':[state.json() for state in StateModel.query.all()]}



class CountryResource(Resource):
    

    def get(self):
        
        return {'countries':[c.json() for c in CountryModel.query.all()]}




class ImageResource(Resource):

    def post(self):
        pic = request.files['pic']

        local = reqparse.RequestParser()
        local.add_argument(
            'filename',
            type=str,
            required=True
        )

        data = local.parse_args()

        if not pic:
            return "No image added"
        
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        image = ImageModel(img=pic.read(),name=filename,mimetype=mimetype,filename=data['filename'])
        image.save()
        return "Image saved"
    

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'image',
            type=int,
            required=False
        )
        data = local.parse_args()

        if data['image']:
            image = ImageModel.find(data['image'])
            if image:
                return image.response()

        image = ImageModel.find(data['id'])
        if image:
            return image.json()

        return "Image not found",404

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True
        )
        data = local.parse_args()
        image = ImageModel.find(**data)

        if image:
            image.delete()
            return "DELETED",200
        return "NOT FOUND",404
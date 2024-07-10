from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    res = {}
    for pic in data:
        res[pic['id']] = pic['pic_url']
    return res
        

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if str(id) == str(pic['id']):
            #return {'pic_url':pic['pic_url']}
            #return pic['pic_url']
            return pic
        else:
            continue
    return {'message':'The picture is not found here'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    for pic in data:
        if pic['id'] == picture['id']:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
        else:
            continue
    data.append(picture)
    return picture, 201




######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic_data = request.get_json()
    for index, pic in enumerate(data):
        if id == pic['id']:
            data[index] = pic_data
            return pic_data, 201
    return {'message':'picture not found'}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if id == pic['id']:
            data.remove(pic)
            return '', 204
    return {'message':'picture not found'}, 404

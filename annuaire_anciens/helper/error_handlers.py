#coding=utf-8
from annuaire_anciens import app
from flask import jsonify

class FormErrorCustom(Exception):
    status_code = 400

    def __init__(self, message, error_dict, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.error_dict = error_dict


    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        if self.error_dict is not None:
            rv['errors'] = self.error_dict
        return rv


@app.errorhandler(FormErrorCustom)
def handle_form_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



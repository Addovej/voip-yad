from flask import current_app as app

from .utils import response


@app.route('/', methods=['GET'])
def main():
    return response('Service is works', 200)

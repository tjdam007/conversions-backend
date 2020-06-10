from functools import wraps

import jwt
from flask import request

from app import app
from ..models import userDao
from ..utils import server_response
from ..utils.constants import ENV, AUTHORIZATION, SECRET_KEY, DEVICE_ID, USER_ID
# Root of Server
from ..utils.messages import KEY_MISSING, USER_NOT_EXISTS, PATH_NOT_EXISTS, AUTHORIZE_ERROR, SERVER_INTERNAL_ERROR, \
    UPLOAD_FILE_LARGE_ERROR


# Base request
@app.route("/")
def root():
    return "{} Server is running".format(app.config.get(ENV)).capitalize()


# authorize each request
def authorize(function):
    @wraps(function)
    def wrapper(*args, **kws):
        authorization = request.headers.get(AUTHORIZATION)
        if authorization is None or len(authorization) <= 0:
            return server_response(error=KEY_MISSING.format(AUTHORIZATION)), 403
        try:
            payload = jwt.decode(authorization, app.config[SECRET_KEY])
            print(f'Auth :{payload}')
            device_id = payload.get(DEVICE_ID)
            user_id = payload.get(USER_ID)
            if userDao.is_user_exists(user_id):
                request.environ[USER_ID] = user_id
                request.environ[DEVICE_ID] = device_id
                return function(*args, **kws)
            else:
                return server_response(error=USER_NOT_EXISTS), 401
        except ValueError as e:
            print(e)
            return server_response(error=USER_NOT_EXISTS), 403

    return wrapper


@app.errorhandler(404)
def page_not_found(e):
    return server_response(error=PATH_NOT_EXISTS), 404


@app.errorhandler(403)
def page_not_found(e):
    return server_response(error=AUTHORIZE_ERROR), 403


@app.errorhandler(413)
def page_not_found(e):
    return server_response(error=UPLOAD_FILE_LARGE_ERROR), 413


@app.errorhandler(500)
def page_not_found(e):
    return server_response(error=SERVER_INTERNAL_ERROR), 500

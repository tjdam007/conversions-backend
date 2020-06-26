from functools import wraps

import jwt
from flask import request

from app import app
from ..models import userDao
from ..utils import server_response
from ..utils.constants import ENV, AUTHORIZATION, SECRET_KEY, DEVICE_ID, USER_ID, APP_VERSION_CODE, APP_PACKAGE, \
    CLIENT_ID, CLIENT_ID_SECRET, APP_PACKAGE_SECRET
# Root of Server
from ..utils.messages import KEY_MISSING, USER_NOT_EXISTS, PATH_NOT_EXISTS, AUTHORIZE_ERROR, SERVER_INTERNAL_ERROR, \
    UPLOAD_FILE_LARGE_ERROR


# authorize each request
def authorize(function):
    @wraps(function)
    def wrapper(*args, **kws):
        app.logger.info('%s %s', request.headers, request.get_data())
        authorization = request.headers.get(AUTHORIZATION)
        if authorization is None:
            return server_response(error=KEY_MISSING.format(AUTHORIZATION)), 403

        client_id = request.headers.get(CLIENT_ID)
        if client_id != app.config[CLIENT_ID_SECRET]:
            return server_response(error=KEY_MISSING.format(CLIENT_ID)), 403

        package = request.headers.get(APP_PACKAGE)
        if package != app.config[APP_PACKAGE_SECRET]:
            return server_response(error=KEY_MISSING.format(APP_PACKAGE)), 403

        app_version_code = request.headers.get(APP_VERSION_CODE)
        if len(app_version_code) <= 0:
            return server_response(error=KEY_MISSING.format(APP_VERSION_CODE)), 403
        try:
            ver = int(app_version_code)
            print(ver)
        except ValueError as e:
            return server_response(error=KEY_MISSING.format(APP_VERSION_CODE)), 403

        try:
            payload = jwt.decode(authorization, app.config[SECRET_KEY])
            device_id = payload.get(DEVICE_ID)
            user_id = payload.get(USER_ID)
            user = userDao.get_user(user_id, device_id)
            if user is not None:
                request.environ[USER_ID] = user.id
                request.environ[DEVICE_ID] = user.device_id
                return function(*args, **kws)
            else:
                return server_response(error=USER_NOT_EXISTS), 401

        except jwt.exceptions.DecodeError as e:
            print(e)
            return server_response(error=USER_NOT_EXISTS), 403
        except ValueError as e:
            print(e)
            return server_response(error=USER_NOT_EXISTS), 403

    return wrapper


# authorize for create user request
def create_authorize(function):
    @wraps(function)
    def wrapper(*args, **kws):
        app.logger.info('%s', request.headers)
        client_id = request.headers.get(CLIENT_ID)
        if client_id != app.config[CLIENT_ID_SECRET]:
            return server_response(error=KEY_MISSING.format(CLIENT_ID)), 403

        package = request.headers.get(APP_PACKAGE)
        if package != app.config[APP_PACKAGE_SECRET]:
            return server_response(error=KEY_MISSING.format(APP_PACKAGE)), 403

        app_version_code = request.headers.get(APP_VERSION_CODE)
        if len(app_version_code) <= 0:
            return server_response(error=KEY_MISSING.format(APP_VERSION_CODE)), 403
        try:
            version = int(app_version_code)
        except ValueError as e:
            return server_response(error=KEY_MISSING.format(APP_VERSION_CODE)), 403
        return function(*args, **kws)

    return wrapper


# Base request
@app.route("/")
def root():
    return "{} Server is running".format(app.config.get(ENV)).capitalize()


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

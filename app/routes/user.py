from flask import request
from werkzeug.exceptions import HTTPException

from app import app
from app.models import userDao
from app.utils import server_response
from app.utils.constants import DEVICE_ID, USER_NAME, EMAIL, PHOTO, CONTENT_TYPE, \
    CONTENT_TYPE_JSON, USER_ID, FCM_TOKEN
from app.utils.messages import KEY_MISSING, CONTENT_TYPE_INVALID, USER_CREATE_SUCCESS, RECORD_EXIST, \
    SOMETHING_WENT_WRONG, FCM_DEVICE_ADDED, USER_RETURN
from . import authorize


# Create user
@app.route("/user/create", methods=['POST'])
def create_user():
    content_type = request.headers.get(CONTENT_TYPE)
    if content_type is None or content_type not in CONTENT_TYPE_JSON:
        return server_response(error=CONTENT_TYPE_INVALID), 400
    data = request.get_json()
    device_id = data.get(DEVICE_ID)
    fcm_token = data.get(FCM_TOKEN)
    if device_id is None:
        return server_response(error=KEY_MISSING.format(DEVICE_ID)), 400
    if fcm_token is None:
        return server_response(error=KEY_MISSING.format(FCM_TOKEN)), 400
    try:
        # create user with device id
        if userDao.is_device_id_exists(device_id):
            return server_response(error=RECORD_EXIST), 409
        success, user = userDao.create_user(device_id, fcm_token)
        if success:
            return server_response(
                data=user.toJSON(),
                message=USER_CREATE_SUCCESS), 200
        else:
            return server_response(
                error=SOMETHING_WENT_WRONG), 500

    except HTTPException as e:
        print(e)
        return server_response(error=SOMETHING_WENT_WRONG), 500


# update user
@app.route("/user/update", methods=['POST'])
@authorize
def update_user():
    content_type = request.headers.get(CONTENT_TYPE)
    if content_type is None or content_type not in CONTENT_TYPE_JSON:
        return server_response(error=CONTENT_TYPE_INVALID), 400
    data = request.get_json()
    user_id = request.environ.get(USER_ID)
    if user_id is None:
        return server_response(error=KEY_MISSING.format(USER_ID)), 400

    user_name = data.get(USER_NAME)
    if user_name is None:
        return server_response(error=KEY_MISSING.format(USER_NAME)), 400

    email = data.get(EMAIL)
    if email is None:
        return server_response(error=KEY_MISSING.format(EMAIL)), 400

    photo = data.get(PHOTO)
    if photo is None:
        return server_response(error=KEY_MISSING.format(PHOTO)), 400
    try:
        old_user = userDao.user_by_email(user_name, email, photo)
        if old_user is None:
            message, user = userDao.update(user_id, user_name, email, photo)
            if user is not None:
                return server_response(data=user.toJSON(), message=message), 200
            else:
                return server_response(error=message), 400
        else:
            # map data to the old user
            userDao.map_data(old_user.id, user_id)
            return server_response(data=old_user.toJSON(), message=USER_RETURN.format(old_user.user_name)), 200
    except HTTPException as e:
        print(e)
        return server_response(error=SOMETHING_WENT_WRONG), 500


@app.route("/user/fcm-token", methods=['POST'])
@authorize
def fcm_token():
    content_type = request.headers.get(CONTENT_TYPE)
    if content_type is None or content_type not in CONTENT_TYPE_JSON:
        return server_response(error=CONTENT_TYPE_INVALID), 400
    data = request.get_json()
    token = data.get(FCM_TOKEN)
    if token is None:
        return server_response(error=KEY_MISSING.format(FCM_TOKEN)), 400
    user_id = request.environ.get(USER_ID)
    success = userDao.update_fcm_token(user_id, token)
    if success:
        return server_response(message=FCM_DEVICE_ADDED), 200
    else:
        return server_response(error=SOMETHING_WENT_WRONG), 400

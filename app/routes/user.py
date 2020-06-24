from flask import request
from werkzeug.exceptions import HTTPException

from app import app
from app.models import userDao
from app.utils import server_response
from app.utils.constants import DEVICE_ID, CONTENT_TYPE, \
    CONTENT_TYPE_JSON, USER_ID, FCM_TOKEN
from app.utils.messages import KEY_MISSING, CONTENT_TYPE_INVALID, USER_CREATE_SUCCESS, RECORD_EXIST, \
    SOMETHING_WENT_WRONG, FCM_DEVICE_ADDED
from . import authorize, create_authorize


# Create user
@app.route("/user/create", methods=['POST'])
@create_authorize
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

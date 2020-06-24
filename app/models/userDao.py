import jwt
from firebase_admin import messaging
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DatabaseError

from app import db, app
from app.models import User, ConvertedFiles
from app.utils.constants import DEVICE_ID, SECRET_KEY
from app.utils.messages import USER_EMAIL_ID_EXISTS, USER_UPDATE_SUCCESS, USER_NOT_EXISTS
from app.utils.push import file_convert_push


# Create User
def create_user(device_id, fcm_token):
    try:
        # Generate JWT token
        auth_token = jwt.encode({DEVICE_ID: device_id}, app.config[SECRET_KEY])
        user = User()
        user.device_id = device_id
        user.fcm_token = fcm_token
        user.auth_token = auth_token
        db.session.add(user)
        db.session.commit()
        return True, user
    except IntegrityError as e:
        print(e)
        return False, None
    except InvalidRequestError as e:
        print(e)
        return False, None


# get user
def get_user(device_id=None):
    try:
        if device_id is not None:
            return db.session.query(User).filter(User.device_id == device_id).first()
        else:
            return None
    except DatabaseError as e:
        print(e)


# check device id
def is_device_id_exists(device_id):
    try:
        return db.session.query(User.device_id).filter(User.device_id == device_id).scalar() is not None
    except DatabaseError as e:
        print(e)
    finally:
        db.session.close()


# check user
def is_user_exists(user_id):
    try:
        return db.session.query(User.id).filter(User.id == user_id).scalar() is not None
    except DatabaseError as e:
        print(e)
    finally:
        db.session.close()


# update user
def update(user_id, user_name, email, photo):
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.user_name = user_name
            user.email = email
            user.photo = photo
            db.session.commit()
            return USER_UPDATE_SUCCESS, user
        else:
            return USER_NOT_EXISTS, None
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return USER_EMAIL_ID_EXISTS, None
    except DatabaseError as e:
        print(e)
        return USER_NOT_EXISTS, None


# create fcm token for user
def update_fcm_token(user_id, token):
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        user.fcm_token = token
        db.session.commit()
        return True
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return False
    except DatabaseError as e:
        print(e)
        return False


# send file conversion push to user
def send_convert_push(file: ConvertedFiles):
    try:
        user: User = User.query.filter(User.id == file.user_id) \
            .order_by(User.id.desc()) \
            .first()
        if user is None:
            print('PUSH SEND FAILED')
        else:
            push_msg = file_convert_push(user.fcm_token, file.id, file.filename, file.from_ext, file.to_ext)
            response = messaging.send(push_msg)
            print(response)
    except Exception as e:
        print(e)

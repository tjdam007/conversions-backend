from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import db
from app.models.enums import Status


# User Table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True)
    user_name = db.Column(String(250), nullable=True)
    device_id = db.Column(String(250), nullable=False, )
    email = db.Column(String(250), nullable=True, unique=True)
    auth_token = db.Column(String(250), nullable=True, unique=True)
    photo = db.Column(String(250), nullable=True)

    def __init__(self, user_name=None, auth_token=None, device_id=None, email=None, photo=None):
        self.device_id = device_id
        self.photo = photo
        self.user_name = user_name
        self.email = email
        self.auth_token = auth_token

    def __repr__(self):
        return '<User %r>' % "name:{} id:{} device_id:{} email:{} photo:{}".format(self.user_name, self.id,
                                                                                   self.device_id, self.email,
                                                                                   self.photo)

    def toJSON(self):
        return {
            "id": self.id,
            "auth_token": self.auth_token,
            "user_name": self.user_name,
            "device_id": self.device_id,
            "email": self.email,
            "photo": self.photo,
        }


# converted files table
class ConvertedFiles(db.Model):
    __tablename__ = "converted_files"
    id = db.Column(Integer, primary_key=True)
    full_filename = db.Column(String(250), nullable=False)
    filename = db.Column(String(250), nullable=False)
    from_ext = db.Column(String(250), nullable=False)
    to_ext = db.Column(String(250), nullable=False)
    from_size = db.Column(Integer, nullable=False)
    upload_path = db.Column(String(250), nullable=False)
    size_unit = db.Column(String(250), nullable=False)
    status = db.Column(String(250), nullable=False)
    to_size = db.Column(Integer, nullable=True)
    convert_path = db.Column(String(250), nullable=True)
    task_id = db.Column(String(250), nullable=True)
    task_attempt = db.Column(Integer, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    def __init__(self, user_id, full_filename, filename, file_ext, to_ext, file_size, upload_path, file_convert_path,
                 size_unit):
        self.user_id = user_id
        self.full_filename = full_filename
        self.filename = filename
        self.from_ext = file_ext
        self.to_ext = to_ext
        self.from_size = file_size
        self.upload_path = upload_path
        self.size_unit = size_unit
        self.status = Status.PENDING.name
        self.convert_path = file_convert_path
        # self.to_size= "NEED TO SAVE AFTER CONVERSION"

    def __repr__(self):
        return '<ConvertedFiles %r>' % f" id:{self.id}" \
                                       f" user_id:{self.user_id}" \
                                       f" filename:{self.full_filename}" \
                                       f" to_size:{self.to_size}" \
                                       f" status:{self.status}"

    def toJSON(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'from_ext': self.from_ext,
            'to_ext': self.to_ext,
            'from_size': self.from_size,
            'status': self.status,
            'to_size': self.to_size,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
            'task_attempt': self.task_attempt
        }


# FCM Token Table
class UserToken(db.Model):
    __tablename__ = "tokens"
    id = db.Column(Integer, primary_key=True)
    token = db.Column(String(250), nullable=False)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def __repr__(self):
        return '<UserToken %r>' % f" id:{self.id}" \
                                  f" token:{self.user_id}" \
                                  f" user_id:{self.full_filename}"


# create all
db.create_all()

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app import db
from app.models import ConvertedFiles


# create file
def create(user_id, full_filename, filename, file_ext, to_ext, file_size, upload_path, file_convert_path, size_unit):
    try:
        file = ConvertedFiles(user_id, full_filename, filename, file_ext, to_ext, file_size, upload_path,
                              file_convert_path, size_unit)
        db.session.add(file)
        db.session.commit()
        db.session.refresh(file)
        db.session.close()
        return True, file
    except IntegrityError as e:
        print(e)
        return False, None
    except InvalidRequestError as e:
        print(e)
        return False, None


# Update File
def update_file(f):
    try:
        file: ConvertedFiles = db.session.query(ConvertedFiles) \
            .filter(ConvertedFiles.id == f.id).first()
        file.to_size = f.to_size
        file.status = f.status
        file.updated_on = db.func.now()
        db.session.commit()
        db.session.close()
        return True
    except IntegrityError as e:
        print(e)
        return False
    except InvalidRequestError as e:
        print(e)
        return False


# Update Task Id of Job
def update_task_id(file_id, task_id):
    try:
        f: ConvertedFiles = db.session.query(ConvertedFiles) \
            .filter(ConvertedFiles.id == file_id).first()
        if f is not None:
            f.task_id = task_id
            db.session.commit()
            db.session.close()
    except IntegrityError as e:
        print(e)
    except InvalidRequestError as e:
        print(e)


# Get single file from user_id and file_id
def getFile(file_id):
    file = db.session.query(ConvertedFiles) \
        .filter(ConvertedFiles.id == file_id) \
        .first()
    db.session.close()
    return file


# Update Conversion attempt for a file
def update_attempt(file: ConvertedFiles):
    f: ConvertedFiles = db.session.query(ConvertedFiles).filter(ConvertedFiles.id == file.id) \
        .first()
    f.task_attempt = file.task_attempt
    db.session.commit()
    db.session.close()


# get all user files
def get_user_files(user_id):
    files = db.session.query(ConvertedFiles).from_statement(
        text("SELECT * FROM converted_files where soft_delete=0 and user_id=:u_id")) \
        .params(u_id=user_id) \
        .all()
    # files = db.session.query(ConvertedFiles) \
    #     .filter(ConvertedFiles.soft_delete == 0, ConvertedFiles.user_id == user_id) \
    #     .order_by(ConvertedFiles.updated_on.desc(), ConvertedFiles.id) \
    #     .all()
    file_dic = []
    for f in files:
        file_dic.append(f.toJSON())
    db.session.close()
    return file_dic


# Delete a file
def delete_file(file_id):
    try:
        f: ConvertedFiles = db.session.query(ConvertedFiles). \
            filter(ConvertedFiles.id == file_id) \
            .first()
        if f is not None:
            f.soft_delete = 1
            db.session.commit()
            db.session.close()
            return True
        return False
    except IntegrityError as e:
        print(e)
        return False
    except InvalidRequestError as e:
        print(e)
        return False

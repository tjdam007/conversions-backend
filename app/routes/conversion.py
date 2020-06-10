import os

from flask import request, send_file
from rq.job import Job
from werkzeug.exceptions import RequestEntityTooLarge, HTTPException
from werkzeug.utils import secure_filename

from app import app
from app.models import userDao, conversionDao, ConvertedFiles
from app.models.enums import SizeUnits
from app.routes import authorize
from app.utils import server_response, allowed_file, get_timestamp
from app.utils.constants import CONTENT_TYPE_MULTIPART, METHOD_POST, FILE, USER_ID, \
    UPLOAD_FOLDER, CONVERTED_FOLDER, CONTENT_TYPE, CONTENT_TYPE_JSON, FILE_ID, ALLOWED_EXTENSIONS
from app.utils.messages import CONTENT_TYPE_INVALID, KEY_MISSING, SOMETHING_WENT_WRONG, FILE_NOT_ALLOWED, \
    USER_NOT_EXISTS, FILE_NAME_EMPTY, FILE_UPLOADED_SUCCESS, FILE_CONVERT_SUCCESS, FILE_CONVERT_FAILED, \
    CONVERSION_NOT_POSSIBLE, INVALID_FILE_ID, FILE_NOT_FOUND, FILE_SIZE_TOO_LARGE
from app.utils.task import convert_file

app.app_context().push()


# upload file
@app.route("/conversion/upload", methods=['POST'])
@authorize
def upload():
    try:
        content_type = request.content_type
        if content_type is None:
            return server_response(error=CONTENT_TYPE_INVALID), 400
        if CONTENT_TYPE_MULTIPART not in content_type:
            return server_response(error=CONTENT_TYPE_INVALID), 400
        if request.method == METHOD_POST:
            if FILE not in request.files:
                return server_response(error=KEY_MISSING.format(FILE)), 400
            user_id = str(request.environ.get(USER_ID))
            if user_id is None:
                return server_response(error=KEY_MISSING.format(USER_ID)), 400

            file = request.files[FILE]
            if file.filename == '':
                return server_response(error=FILE_NAME_EMPTY), 400
            if not allowed_file(file.filename):
                return server_response(error=FILE_NOT_ALLOWED), 400

            if not userDao.is_user_exists(user_id):
                return server_response(error=USER_NOT_EXISTS), 400

            # to_ext = ".pdf"
            # if TO_EXT in request.form:
            #     to_ext = request.form.get(TO_EXT)

            full_filename = secure_filename(file.filename)
            # upload folder path
            file_upload_dir = os.path.join(app.config[UPLOAD_FOLDER], user_id)
            # convert folder path
            file_convert_dir = os.path.join(app.config[CONVERTED_FOLDER], user_id)

            # create upload dir for user
            if not os.path.exists(file_upload_dir):
                os.makedirs(file_upload_dir)

            # create convert dir for user
            if not os.path.exists(file_convert_dir):
                os.makedirs(file_convert_dir)

            # name and extension
            filename_only, file_ext = os.path.splitext(full_filename)
            # timestamp
            timestamp = get_timestamp()
            # create uploaded file name
            temp_upload_file_name = '{}{}'.format(timestamp, file_ext)
            # create upload path
            file_upload_path = os.path.join(file_upload_dir, temp_upload_file_name)
            # save uploaded file
            file.save(file_upload_path)
            file_size = os.stat(file_upload_path).st_size

            # create convert filename
            temp_convert_file_name = '{}.pdf'.format(timestamp)
            # create convert path
            file_convert_path = os.path.join(file_convert_dir, temp_convert_file_name)

            size_unit = SizeUnits.BYTES.name

            success, file_data = conversionDao.create(user_id, full_filename, filename_only, file_ext, '.pdf',
                                                      file_size,
                                                      file_upload_path, file_convert_path, size_unit)
            if success:
                # Add task for file conversion
                job: Job = app.queue.enqueue(convert_file, file_data)
                # update task id
                conversionDao.update_task_id(file_data.id, job.id)
                return server_response(message=FILE_UPLOADED_SUCCESS), 200
            else:
                return server_response(error=SOMETHING_WENT_WRONG), 500
        else:
            return server_response(error=SOMETHING_WENT_WRONG), 500
    except RequestEntityTooLarge as e:
        print(e)
        return server_response(error=FILE_SIZE_TOO_LARGE), 400


# Convert a user file on demand
@app.route('/conversion/convert-attempt', methods=['POST'])
@authorize
def convert_attempt():
    content_type = request.headers.get(CONTENT_TYPE)
    if content_type is None or content_type not in CONTENT_TYPE_JSON:
        return server_response(error=CONTENT_TYPE_INVALID), 403

    user_id = request.environ.get(USER_ID)
    data = request.get_json()
    file_id = data.get(FILE_ID)

    if user_id is None:
        return server_response(error=KEY_MISSING.format(USER_ID)), 400

    if file_id is None:
        return server_response(error=KEY_MISSING.format(FILE_ID)), 400

    file: ConvertedFiles = conversionDao.getFile(file_id, user_id)
    if file is None:
        return server_response(error=CONVERSION_NOT_POSSIBLE), 400

    if file.task_attempt == 3:
        return server_response(error=CONVERSION_NOT_POSSIBLE), 400

    success = convert_file(file)
    if success:
        return server_response(message=FILE_CONVERT_SUCCESS), 200
    else:
        file.task_attempt += 1
        conversionDao.update_attempt(file)
        return server_response(message=FILE_CONVERT_FAILED), 500


# Get Converted files <int:post_id>'
@app.route("/conversion/get-converted-files/<int:file_id>", methods=['GET'])
@authorize
def get_converted_file(file_id):
    if not isinstance(file_id, int):
        return server_response(error=INVALID_FILE_ID), 403
    user_id = request.environ.get(USER_ID)
    file = conversionDao.getFile(file_id, user_id)
    if file is not None:
        return send_file(file.convert_path, as_attachment=True,
                         attachment_filename=f'{file.filename}{file.to_ext}'), 200
    else:
        return server_response(error=FILE_NOT_FOUND), 403


# Get all files for user
@app.route('/conversion/get-all-files', methods=['GET'])
@authorize
def get_all_files():
    try:
        user_id = request.environ.get(USER_ID)
        files = conversionDao.get_user_files(user_id)
        return server_response(data=files), 200
    except HTTPException as e:
        print(e)
        return server_response(error=SOMETHING_WENT_WRONG), 500


@app.route('/conversion/allowed-file')
def app_allowed_file():
    ext_list = list(app.config[ALLOWED_EXTENSIONS])
    return server_response(data=ext_list), 200


# Delete a file
@app.route('/conversion/delete/<int:file_id>', methods=['POST'])
@authorize
def soft_delete(file_id):
    if not isinstance(file_id, int):
        return server_response(error=INVALID_FILE_ID), 403
    user_id = request.environ.get(USER_ID)
    success = conversionDao.delete_file(file_id, user_id)
    if success:
        return server_response(message=FILE_CONVERT_SUCCESS), 200
    else:
        return server_response(error=FILE_NOT_FOUND), 403

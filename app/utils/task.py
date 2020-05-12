import os

from app import app
from app.models import ConvertedFiles, Status, conversionDao, userDao
from app.utils.constants import CONVERTED_FOLDER, WRITER_PDF_EXPORT, IMPRESS_PDF_EXPORT, CALC_PDF_EXPORT, \
    DRAW_PDF_EXPORT


# Convert file task
def convert_file(file: ConvertedFiles):
    file_convert_dir = os.path.join(app.config[CONVERTED_FOLDER], str(file.user_id))

    if not os.path.exists(file_convert_dir):
        os.makedirs(file_convert_dir)

    success_message = f'convert {file.upload_path} -> {file.convert_path} using filter : {get_filter(file)}'.strip()
    std = os.popen(
        f'soffice --convert-to pdf {file.upload_path} --outdir {file_convert_dir}')
    output = std.read().strip()
    if success_message.lower() == output.lower():
        file.status = Status.CONVERTED.name
        file.to_size = os.stat(file.convert_path).st_size
    else:
        file.status = Status.FAILED.name
        file.to_size = 0

    print(file)
    success = conversionDao.update_file(file)
    if success:
        print("DB UPDATED", file)
        userDao.send_convert_push(file)
    else:
        print("FAILED TO UPDATE DB", file)
    return success


# get export filters
def get_filter(file: ConvertedFiles):
    if file.from_ext in app.config[WRITER_PDF_EXPORT]:
        return WRITER_PDF_EXPORT
    elif file.from_ext in app.config[IMPRESS_PDF_EXPORT]:
        return IMPRESS_PDF_EXPORT
    elif file.from_ext in app.config[CALC_PDF_EXPORT]:
        return CALC_PDF_EXPORT
    elif file.from_ext in app.config[DRAW_PDF_EXPORT]:
        return DRAW_PDF_EXPORT
    else:
        "None"

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    UPLOAD_FOLDER = '{}/files/uploads'.format(os.path.abspath(os.curdir))
    CONVERTED_FOLDER = '{}/files/converted'.format(os.path.abspath(os.curdir))
    GOOGLE_CERTIFICATE_FILE_PATH = "{}/conversions-01-firebase-adminsdk-trny6-1dd4d3bcca.json".format(
        os.path.abspath(os.curdir))

    ALLOWED_EXTENSIONS = {'rtf', 'docx', 'doc', 'odt', 'json', 'xml', 'gif', 'jpg', 'jpeg', 'png', 'tiff',
                          'xls', 'ods', 'csv', 'xlsx', 'ppt', 'odp', 'txt'}

    WRITER_PDF_EXPORT = {'.rtf', '.docx', '.doc', '.odt', '.json', '.xml', '.txt'}  # writer_pdf_Export
    DRAW_PDF_EXPORT = {'.gif', '.jpg', '.jpeg', '.png', '.tiff'}  # draw_pdf_Export
    CALC_PDF_EXPORT = {'.xls', '.ods', '.csv', '.xlsx'}  # CALC_PDF_EXPORT
    IMPRESS_PDF_EXPORT = {'.ppt', '.odp'}  # impress_pdf_Export


class ProductionConfig(AppConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/prod_conversion"


class DevelopmentConfig(AppConfig):
    DEBUG = True
    SECRET_KEY = b'\xe0\x9fj\xc5qxl\x19'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/dev_conversion"


class TestingConfig(AppConfig):
    TESTING = True
    SECRET_KEY = "b'\xe0\x9fj\xc5qxl\x19'"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/dev_conversion"

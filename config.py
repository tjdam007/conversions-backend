import os

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    LOGS_FILE = '{}/logs/errorlogs.txt'.format(os.path.abspath(os.curdir))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID_SECRET = '862321218592-t53fg9aibdtc4leb1ueqrkgpp5njrpl7.apps.googleusercontent.com'
    APP_PACKAGE_SECRET = "com.dev4solutions.conversions.debug"
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'\xe0\x9fj\xc5qxl\x19'
    JSONIFY_PRETTYPRINT_REGULAR = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MBs
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
    APP_PACKAGE_SECRET = "com.dev4solutions.conversions"
    SECRET_KEY = '0e4c541b3342df5994682825d0785b2a'
    AUTH_SECRET = '3814d1fe74d93cc1a82ffdf8653e1390'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/prod_conversion"


class DevelopmentConfig(AppConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/dev_conversion"


class TestingConfig(AppConfig):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://crud_conversion:Z/?^G~jW*ad`.6AY@localhost/dev_conversion"

import os, binascii

dirname = os.path.dirname(__file__)

class Config(object):
    UPLOAD_FOLDER = os.path.join(dirname, 'app/static/upload')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = binascii.hexlify(os.urandom(24))
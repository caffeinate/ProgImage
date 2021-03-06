class BaseConfig(object):
    DEBUG = False
    APP_TITLE = "ProgImage"
    LOGGING_SYSLOG_LEVEL = None # string, e.g. "INFO"
    LOGGING_EMAIL_LEVEL = None
    FILEBASE = "" # depends on which implementation of FileBase is being used

class Config():
    SECRET_KEY = '64h743hz4589nfdg495jZ'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.web.de'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'nici.hahn@web.de'
    MAIL_PASSWORD = '#.Dose96Ncls'
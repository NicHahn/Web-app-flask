from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

#page not found
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404     #second parameter is default 200

#Forbidden page
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403     #second parameter is default 200

#generall server errror, not descriptive
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500     #second parameter is default 200
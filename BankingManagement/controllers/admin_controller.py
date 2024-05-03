from flask import Blueprint, render_template, request

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin', methods = ['GET'])
def adminIndex():
    if request.method == 'GET':
        return render_template('admin.html')
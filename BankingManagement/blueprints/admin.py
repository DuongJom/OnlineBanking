from flask import Blueprint, render_template, request

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin/home', methods = ['GET'])
def admin_home():
    if request.method == 'GET':
        return render_template('admin/home.html')
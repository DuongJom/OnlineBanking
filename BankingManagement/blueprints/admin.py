from flask import Blueprint, render_template, request, jsonify

from models import database

from helpers import login_required, paginator

admin_blueprint = Blueprint('admin', __name__)

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
services = db['services']

@admin_blueprint.route('/admin/user', methods = ['GET'])
def admin_user():
    if request.method == 'GET':
        return render_template('admin/user.html')
    
@admin_blueprint.route('/admin/account', methods = ['GET'])
@login_required
def account():
    if request.method == 'GET':
        return render_template('admin/account.html')
    
@admin_blueprint.route('/admin/employee', methods = ['GET'])
def employee():
    if request.method == 'GET':
        return render_template('admin/employee.html')
    
@admin_blueprint.route('/admin/branch', methods = ['GET'])
def branch():
    if request.method == 'GET':
        return render_template('admin/branch.html')
    
@admin_blueprint.route('/admin/chart', methods = ['GET'])
def chart():
    if request.method == 'GET':
        return render_template('admin/chart.html')
    
@admin_blueprint.route('/admin', methods=['GET'])
@login_required
def admin():
    page = request.args.get('page', 1, int)
    dataType = request.args.get('dataType')

    items = []

    if dataType == 'account':
        items = list(accounts.find({}, {'_id': 0})) 
    if dataType == 'user':
        items = list(users.find({}, {'_id': 0}))
    
    pagination = paginator(page, items)

    return jsonify({'items': pagination['render_items'], 'total_pages': pagination['total_pages']})
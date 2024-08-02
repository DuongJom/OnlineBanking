from flask import Blueprint, render_template, request, jsonify
from bson import ObjectId

from models import database

from helpers import login_required

admin_blueprint = Blueprint('admin', __name__)   

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
services = db['services']
employees = db['employees']

@admin_blueprint.route('/admin', methods=['GET'])
@login_required
def admin():
    per_page = 10
    page = request.args.get('page', 1, int)
    dataType = request.args.get('dataType')
    collection = None
    items = []
    total_pages = 0

    # decide which collection to query
    if dataType == 'account':
        collection = accounts
    elif dataType == 'user':
        collection = users
    elif dataType == 'branch':
        collection = branches
    elif dataType == 'employee':
        collection = employees

    # query for list of data and total pages
    total_pages = (collection.count_documents({}) + per_page - 1) // per_page
    items_cursor = collection.find({}).skip((page-1)*per_page).limit(per_page)

    # convert ObjectId '_id' to string '_id'
    for item in items_cursor:
        if '_id' in item:
            item['_id'] = str(item['_id'])
        items.append(item)

    return jsonify({'items': items, 'total_pages': total_pages})

# Start admin_account

@admin_blueprint.route('/admin/account', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/account/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/account/<page>/<id>', methods=['GET'])
@login_required
def account(page, id):
    if request.method == 'GET':
        if page == "add":
            return render_template('admin/add_account.html')
        elif page == "view" and id is not None:
            account_id = ObjectId(id)
            viewed_account = accounts.find_one({"_id": account_id})
            return render_template('admin/view_account.html', account = viewed_account)
        elif page == "edit" and id is not None:
            account_id = ObjectId(id)
            edited_account = accounts.find_one({"_id": account_id})
            return render_template('admin/edit_account.html', account = edited_account)
        return render_template('admin/account.html')

# End admin_account

@admin_blueprint.route('/admin/user', methods = ['GET'])
def admin_user():
    if request.method == 'GET':
        return render_template('admin/user.html')
    
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
    
@admin_blueprint.route('/admin/news', methods = ['GET'])
def news():
    if request.method == 'GET':
        return render_template('admin/news.html')




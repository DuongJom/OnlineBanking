from flask import Blueprint, render_template, request, jsonify
from bson import ObjectId
from datetime import datetime

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

@admin_blueprint.route('/admin/user', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/user/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/user/<page>/<id>', methods=['GET'])
@login_required
def user(page, id):
    if request.method == 'GET':
        if page == "view" and id is not None:
            expiredDate = None
            issuanceDate = None
            user_id = ObjectId(id)
            viewed_user = users.find_one({"_id": user_id})
            if(viewed_user['Card']):
                expiredDate = datetime.fromisoformat(viewed_user['Card']['ExpiredDate']).date()
                issuanceDate = datetime.fromisoformat(viewed_user['Card']['IssuanceDate']).date()
            return render_template('admin/view_user.html', user = viewed_user, expiredDate = expiredDate, issuanceDate = issuanceDate)
        elif page == "edit" and id is not None:
            user_id = ObjectId(id)
            edited_user = users.find_one({"_id": user_id}) 
            return render_template('admin/edit_user.html', user = edited_user)
        return render_template('admin/user.html')
    
@admin_blueprint.route('/admin/employee', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/employee/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/employee/<page>/<id>', methods=['GET'])
@login_required
def employee(page, id):
    if request.method == 'GET':
        if page == "add":
            return render_template('admin/add_employee.html')
        elif page == "view" and id is not None:
            employee_id = ObjectId(id)
            viewed_employee = users.find_one({"_id": employee_id})
            return render_template('admin/view_employee.html', employee = viewed_employee)
        elif page == "edit" and id is not None:
            employee_id = ObjectId(id)
            edited_employee = users.find_one({"_id": employee_id}) 
            return render_template('admin/edit_employee.html', employee = edited_employee)
        return render_template('admin/employee.html')
    
@admin_blueprint.route('/admin/branch', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/branch/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/branch/<page>/<id>', methods=['GET'])
@login_required
def branch(page, id):
    if request.method == 'GET':
        if page == "add":
            return render_template('admin/add_branch.html')
        elif page == "view" and id is not None:
            branch_id = ObjectId(id)
            viewed_branch = users.find_one({"_id": branch_id})
            return render_template('admin/view_branch.html', branch = viewed_branch)
        elif page == "edit" and id is not None:
            branch_id = ObjectId(id)
            edited_branch = users.find_one({"_id": branch_id}) 
            return render_template('admin/edit_branch.html', branch = edited_branch)
        return render_template('admin/branch.html')
    
@admin_blueprint.route('/admin/chart', methods = ['GET'])
def chart():
    if request.method == 'GET':
        return render_template('admin/chart.html')
    
@admin_blueprint.route('/admin/news', methods = ['GET'])
def news():
    if request.method == 'GET':
        return render_template('admin/news.html')
    
        
@admin_blueprint.route('/admin/import-data', methods = ['GET'])
def import_data():
    if request.method == 'GET':
        return render_template('admin/import_data.html')




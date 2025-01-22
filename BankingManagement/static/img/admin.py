from flask import Blueprint, render_template, request, jsonify, redirect, flash, session, send_file
from bson import ObjectId
from datetime import datetime
from io import BytesIO
import pandas as pd

from models import database, address, user as u, card, account as acc
from helpers.helpers import login_required, issueNewCard, generate_login_info, send_email,get_file_extension
from helpers.admin import create_accounts, generate_export_data
from enums.card_type import CardType
from enums.deleted_type import DeletedType
from enums.data_type import DataType
from message import messages_success, messages_failure

admin_blueprint = Blueprint('admin', __name__)   

db = database.Database().get_db()
accounts = db['accounts']
addresses = db['address']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
employees = db['employee']
news = db['news']
login_methods = db['login_methods']
transfer_methods = db['transfer_methods']
roles = db['roles']
card_types = db['card_types']

@admin_blueprint.route('/admin', methods=['POST'])
@login_required
def admin():
    page = request.json.get('page', 1)
    dataType = request.json.get('dataType')
    filters = request.json.get('filter')

    for key, value in filters.items():
        if isinstance(value, str) and value.isdigit(): 
            filters[key] = int(value)
        elif isinstance(value, (int, float)):  
            filters[key] = int(value)

    collection = None
    items = []
    total_pages = 0

    if dataType == DataType.ACCOUNT.value:
        collection = accounts
    elif dataType == DataType.USER.value:
        collection = users
    elif dataType == DataType.BRANCH.value:
        collection = branches
    elif dataType == DataType.EMPLOYEE.value:
        collection = employees
    elif dataType == DataType.NEWS.value:
        collection = news

    # Calculate total pages and fetch items
    per_page = 10
    total_documents = collection.count_documents({})
    total_pages = (total_documents + per_page - 1) // per_page
    items_cursor = collection.find(filters).skip((page - 1) * per_page).limit(per_page)

    # Convert ObjectId to string for JSON response
    for item in items_cursor:
        if '_id' in item:
            item['_id'] = str(item['_id'])
        items.append(item)

    return jsonify({'items': items, 'total_pages': total_pages})

# Start admin_account

@admin_blueprint.route('/admin/account', defaults={'page': None, 'id': None}, methods=['GET', 'POST'])
@admin_blueprint.route('/admin/account/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/account/<page>/<id>', methods=['GET'])
@login_required
def account(page, id):
    if request.method == 'GET':
        loginMethods = login_methods.find()
        transferMethods = transfer_methods.find()
        _roles = roles.find()
        _branches = branches.find()
        if page == "add":
            return render_template('admin/account/add_account.html', 
                                   loginMethods = loginMethods, 
                                   transferMethods = transferMethods, 
                                   roles = _roles,
                                   branches = _branches)
        elif page == "view" and id is not None:
            account_id = ObjectId(id)
            viewed_account = accounts.find_one({"_id": account_id})
            login_values = [method["Value"] for method in viewed_account["LoginMethod"]]
            transfer_values = [method["Value"] for method in viewed_account["TransferMethod"]]
            
            return render_template('admin/account/view_account.html', 
                                   account = viewed_account,
                                   login_values = login_values,
                                   transfer_values = transfer_values,
                                   loginMethods = loginMethods, 
                                   transferMethods = transferMethods,)
        elif page == "edit" and id is not None:
            account_id = ObjectId(id)
            edited_account = accounts.find_one({"_id": account_id})
            login_values = []
            transfer_values = []
            login_values = [method["Value"] for method in edited_account["LoginMethod"]]
            transfer_values = [method["Value"] for method in edited_account["TransferMethod"]]

            return render_template('admin/account/edit_account.html', 
                                   account = edited_account,
                                   loginMethods = loginMethods, 
                                   transferMethods = transferMethods, 
                                   roles = _roles,
                                   branches = _branches,
                                   login_values = login_values,
                                   transfer_values = transfer_values)
        return render_template('admin/account/account.html')
    elif request.method == 'POST':
        admin_id = session.get("account_id")
        # Account info
        card_type = card_types.find_one({"TypeValue": CardType.CREDITS.value}, {"_id":0})
        card_info = issueNewCard()
        role = roles.find_one({"Value": int(request.form['role'])}, {"_id":0})

        loginMethodTypeList = list(map(int, request.form.getlist("loginMethod")))
        transferMethodTypeList = list(map(int, request.form.getlist("transferMethod")))

        loginMethods = list(login_methods.find(
            {'Value': {'$in': loginMethodTypeList}}, 
            {'_id': 0}  
        ))

        transferMethods = list(transfer_methods.find(
            {'Value': {'$in': transferMethodTypeList}}, 
            {'_id': 0}  
        ))
        request_branch = None

        try:
            request_branch = branches.find_one({"BranchName": request.form['branch']}, {"_id":0})
        except KeyError:
            request_branch = None

        # User info
        name = request.form['name']
        sex = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']    

        #Login info
        loginInfo = generate_login_info(email, phone)

        # Address
        street = request.form['street']
        ward = request.form['ward']
        district = request.form['district']
        city = request.form['city']
        country = request.form['country']

        # check if user input email and password or not
        error = None
        # check if email or username already exist
        existEmail = users.find_one({"Email": email})
        existPhone = users.find_one({"Phone": phone})

        if existEmail:
            error = messages_failure['email_existed'].format(email) 
        elif existPhone:
            error = messages_failure['phone_existed'].format(phone)
        
        if error:
            flash(error, 'error')
            return redirect("/admin/account/add")
        
        new_card = card.Card(cardNumber=card_info['cardNumber'], cvv=card_info['cvvNumber'], type=card_type, createdBy = admin_id)
        
        new_address = address.Address(street = street, ward = ward, district = district, city = city, country = country, createdBy = admin_id)

        new_user = u.User(name = name, sex = sex, address = new_address.to_json(), phone = phone, email = email, card = new_card.to_json(),
                          createdBy = admin_id)

        new_account = acc.Account(accountNumber = card_info['accountNumber'], branch = request_branch, user = new_user.to_json(),
                                  username = loginInfo['Username'], password = loginInfo['Password'], role = role,
                                  transferMethod = transferMethods, loginMethod = loginMethods, createdBy = admin_id)

        cards.insert_one(new_card.to_json())
        addresses.insert_one(new_address.to_json())
        users.insert_one(new_user.to_json())
        accounts.insert_one(new_account.to_json())

        html = render_template('email/send_Login_Info.html', username = loginInfo['Username'], password = loginInfo['Password'])
        attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
        subject = "Send login information"
        send_email(email, subject, html, attachments=attachments)
        flash(messages_success['register_success'].format(email), 'success')
        return redirect('/admin/account/add')
    
@admin_blueprint.route('/admin/account/delete/<id>', methods=['POST'])
@login_required
def delete_account(id):
    if request.method == 'POST':
        account_id = ObjectId(id)
        _account = accounts.find_one({"_id": account_id})
        accounts.update_one(
            {'_id': account_id},
            {"$set": {"IsDeleted": DeletedType.DELETED.value}
        })      
        flash(messages_success['delete_success'].format(_account["Username"]), 'success') 
    return redirect('/admin/account')

@admin_blueprint.route('/admin/edit_account', methods=['POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        admin_id = session.get("account_id")
        _id = request.form.get("account_id")
        id = ObjectId(_id)
        role = roles.find_one({"Value": int(request.form['role'])}, {"_id":0})

        loginMethodTypeList = list(map(int, request.form.getlist("loginMethod")))
        transferMethodTypeList = list(map(int, request.form.getlist("transferMethod")))

        status = int(request.form.get("status"))

        loginMethods = list(login_methods.find(
            {'Value': {'$in': loginMethodTypeList}}, 
            {'_id': 0}  
        ))

        transferMethods = list(transfer_methods.find(
            {'Value': {'$in': transferMethodTypeList}}, 
            {'_id': 0}  
        ))

        request_branch = None

        try:
            request_branch = branches.find_one({"BranchName": request.form['branch']}, {"_id": 0})
        except KeyError:
            request_branch = None

        accounts.update_one(
            {'_id': id},
            {"$set": {
                "Role": role,
                "LoginMethod": loginMethods,
                "TransferMethod": transferMethods,
                "Branch": request_branch,
                "IsDeleted": status,
                "ModifiedBy": admin_id
            }}
        )

        flash(messages_success["update_success"].format("Account"), 'success')
        return redirect("/admin/account")

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
            if viewed_user and viewed_user['Card']:
                expiredDate = datetime.fromisoformat(viewed_user['Card']['ExpiredDate']).date()
                issuanceDate = datetime.fromisoformat(viewed_user['Card']['IssuanceDate']).date()
            return render_template('admin/user/view_user.html', 
                                   user = viewed_user, 
                                   expiredDate = expiredDate, 
                                   issuanceDate = issuanceDate)
        elif page == "edit" and id is not None:
            user_id = ObjectId(id)
            edited_user = users.find_one({"_id": user_id}) 
            return render_template('admin/user/edit_user.html', user = edited_user)
        return render_template('admin/user/user.html')
    
@admin_blueprint.route('/admin/employee', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/employee/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/employee/<page>/<id>', methods=['GET'])
@login_required
def employee(page, id):
    if request.method == 'GET':
        if page == "add":
            return render_template('admin/employee/add_employee.html')
        elif page == "view" and id is not None:
            employee_id = ObjectId(id)
            viewed_employee = users.find_one({"_id": employee_id})
            return render_template('admin/employee/view_employee.html', employee = viewed_employee)
        elif page == "edit" and id is not None:
            employee_id = ObjectId(id)
            edited_employee = users.find_one({"_id": employee_id}) 
            return render_template('admin/employee/edit_employee.html', employee = edited_employee)
        return render_template('admin/employee/employee.html')
    
@admin_blueprint.route('/admin/branch', defaults={'page': None, 'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/branch/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/branch/<page>/<id>', methods=['GET'])
@login_required
def branch(page, id):
    if request.method == 'GET':
        if page == "add":
            return render_template('admin/branch/add_branch.html')
        elif page == "view" and id is not None:
            branch_id = ObjectId(id)
            viewed_branch = users.find_one({"_id": branch_id})
            return render_template('admin/branch/view_branch.html', branch = viewed_branch)
        elif page == "edit" and id is not None:
            branch_id = ObjectId(id)
            edited_branch = users.find_one({"_id": branch_id}) 
            return render_template('admin/branch/edit_branch.html', branch = edited_branch)
        return render_template('admin/branch/branch.html')
    
@admin_blueprint.route('/admin/chart', methods = ['GET'])
def chart():
    if request.method == 'GET':
        return render_template('admin/general/chart.html')
    
@admin_blueprint.route('/admin/news', methods = ['GET'])
def admin_news():
    if request.method == 'GET':
        return render_template('admin/news/news.html')
    
@admin_blueprint.route('/admin/<data_type>/import', methods=['POST'])
@login_required
def import_data(data_type):
    if request.method == 'POST':
        file = request.files['file']
        ext = get_file_extension(file.filename)

        if ext == 'csv':
            df = pd.read_csv(BytesIO(file.read()))
        elif ext == 'xlsx':
            df = pd.read_excel(BytesIO(file.read()), engine='openpyxl')
        
        data = df.to_dict(orient='records')
        res = create_accounts(data)
    return jsonify(res)

@admin_blueprint.route('/admin/export-data/<dataType>', methods=['POST'])
@login_required
def export_data(dataType):
    filters = request.json.get('filter')
    file_type = request.json.get('file_type')
    now = datetime.now()
    file_name = f"{now.year}{now.month}{now.day}_{dataType}"
    data = generate_export_data(dataType=dataType, file_type=file_type, filters=filters)
    return send_file(data['output'], as_attachment=True, download_name=file_name, mimetype=data['mime'])
import pandas as pd
from bson import ObjectId
from datetime import datetime
from io import BytesIO
from flask import Blueprint, render_template, jsonify, redirect, flash, send_file, request, session

from models.database import Database
from models.address import Address
from models.user import User
from models.card import Card
from models.account import Account
from enums.card_type import CardType
from enums.deleted_type import DeletedType
from enums.data_type import DataType
from enums.admin_page_type import PageType
from enums.file_type import FileType
from message import messages_success, messages_failure
from helpers.helpers import login_required, issueNewCard, generate_login_info, send_email,get_file_extension
from helpers.admin import create_accounts, generate_export_data

admin_blueprint = Blueprint('admin', __name__)

db = Database().get_db()
accounts = db['accounts']
addresses = db['addresses']
users = db['users']
branches = db['branches']
cards = db['cards']
employees = db['employees']
news = db['news']
login_methods = db['login_methods']
transfer_methods = db['transfer_methods']
roles = db['roles']
card_types = db['card_types']

@admin_blueprint.route('/admin', methods=['POST'])
@login_required
def admin():
    page = request.json.get('page', 1)
    data_type = request.json.get('dataType')
    criteria = request.json.get('filter')

    for key, value in criteria.items():
        if isinstance(value, str) and value.isdigit(): 
            criteria[key] = int(value)
        elif isinstance(value, (int, float)):  
            criteria[key] = int(value)

    collection = None
    lst_display_items = []
    total_pages = 0

    if data_type == DataType.ACCOUNT.value:
        collection = accounts
    elif data_type == DataType.USER.value:
        collection = users
    elif data_type == DataType.BRANCH.value:
        collection = branches
    elif data_type == DataType.EMPLOYEE.value:
        collection = employees
    elif data_type == DataType.NEWS.value:
        collection = news

    # Calculate total pages and fetch items
    items_per_page = 10
    total_documents = collection.count_documents({})
    total_pages = (total_documents + items_per_page - 1) // items_per_page
    items = collection.find(criteria).skip((page - 1) * items_per_page).limit(items_per_page)

    # Convert ObjectId to string for JSON response
    for item in items:
        if '_id' in item:
            item['_id'] = str(item['_id'])
        lst_display_items.append(item)
    return jsonify({'items': lst_display_items, 'total_pages': total_pages})

@admin_blueprint.route('/admin/account', defaults={'page': None, 'id': None}, methods=['GET', 'POST'])
@admin_blueprint.route('/admin/account/<page>', defaults={'id': None}, methods=['GET'])
@admin_blueprint.route('/admin/account/<page>/<id>', methods=['GET'])
@login_required
def account(page, id):
    if request.method == 'GET':
        lst_login_methods = login_methods.find()
        lst_transfer_methods = transfer_methods.find()
        lst_roles = roles.find()
        lst_branches = branches.find()

        if page == PageType.ADD.value:
            return render_template('admin/account/add_account.html', 
                                   login_methods = lst_login_methods, 
                                   transfer_methods = lst_transfer_methods, 
                                   roles = lst_roles,
                                   branches = lst_branches)
        
        if page == PageType.VIEW.value and id is not None:
            account_id = ObjectId(id)
            viewed_account = accounts.find_one({"_id": account_id})
            login_values = [method["Value"] for method in viewed_account["LoginMethod"]]
            transfer_values = [method["Value"] for method in viewed_account["TransferMethod"]]
            
            return render_template('admin/account/view_account.html', 
                                   account = viewed_account,
                                   login_values = login_values,
                                   transfer_values = transfer_values,
                                   login_methods = lst_login_methods, 
                                   transfer_methods = lst_transfer_methods)
        
        if page == PageType.EDIT.value and id is not None:
            account_id = ObjectId(id)
            edited_account = accounts.find_one({"_id": account_id})
            login_values = [method["Value"] for method in edited_account["LoginMethod"]]
            transfer_values = [method["Value"] for method in edited_account["TransferMethod"]]

            return render_template('admin/account/edit_account.html', 
                                   account = edited_account,
                                   login_methods = lst_login_methods, 
                                   transfer_methods = lst_transfer_methods, 
                                   roles = lst_roles,
                                   branches = lst_branches,
                                   login_values = login_values,
                                   transfer_values = transfer_values)
        return render_template('admin/account/account.html')

    try:
        log_in_id = session.get("account_id")
        # Account info
        card_type = card_types.find_one({"TypeValue": CardType.CREDITS.value}, {"_id":0})
        card_info = issueNewCard()
        role = roles.find_one({"Value": int(request.form['role'])}, {"_id":0})

        lst_login_method_type = list(map(int, request.form.getlist("loginMethod")))
        lst_transfer_method_type = list(map(int, request.form.getlist("transferMethod")))

        lst_login_methods = list(login_methods.find(
            {'Value': {'$in': lst_login_method_type}}, 
            {'_id': 0}  
        ))

        lst_transfer_methods = list(transfer_methods.find(
            {'Value': {'$in': lst_transfer_method_type}}, 
            {'_id': 0}  
        ))

        request_branch = branches.find_one({"BranchName": request.form['branch']}, {"_id":0})
        # User info
        name = request.form.get('name')
        sex = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email') 

        #Login info
        login_info = generate_login_info(email, phone)

        # Address
        street = request.form.get('street')
        ward = request.form.get('ward')
        district = request.form.get('district')
        city = request.form.get('city')
        country = request.form.get('country')

        # check if user input email and password or not
        error_message = None
        # check if email or username already exist
        is_exist_email = True if users.find_one({"Email": email}) else False
        is_exist_phone = True if users.find_one({"Phone": phone}) else False
        
        if is_exist_email:
            error_message = messages_failure['email_existed'].format(email) 
        elif is_exist_phone:
            error_message = messages_failure['phone_existed'].format(phone)
            
        if error_message:
            flash(error_message, 'error')
            return redirect("/admin/account/add")
            
        new_card = Card(
            cardNumber = card_info['cardNumber'], 
            cvv = card_info['cvvNumber'], 
            type = card_type, 
            createdBy = log_in_id
        )
            
        new_address = Address(
            street = street, 
            ward = ward, 
            district = district, 
            city = city, 
            country = country, 
            createdBy = log_in_id
        )

        new_user = User(
            name = name, 
            sex = sex, 
            address = new_address.to_json(), 
            phone = phone, 
            email = email, 
            card = new_card.to_json(),
            createdBy = log_in_id
        )

        new_account = Account(
            accountNumber = card_info['accountNumber'], 
            branch = request_branch, 
            user = new_user.to_json(),
            username = login_info['Username'], 
            password = login_info['Password'], 
            role = role,
            transferMethod = lst_transfer_methods, 
            loginMethod = lst_login_methods, 
            createdBy = log_in_id
        )

        cards.insert_one(new_card.to_json())
        addresses.insert_one(new_address.to_json())
        users.insert_one(new_user.to_json())
        accounts.insert_one(new_account.to_json())

        html = render_template('email/send_login_info.html', username = login_info['Username'], password = login_info['Password'])
        attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
        subject = "Send login information"
        send_email(email, subject, html, attachments=attachments)
        flash(messages_success['register_success'].format(email), 'success')
    except KeyError:
        flash(messages_failure['internal_error'], 'error')
    return redirect('/admin/account/add')   
    
@admin_blueprint.route('/admin/account/delete/<id>', methods=['POST'])
@login_required
def delete_account(id):
    account_id = ObjectId(id)
    account = accounts.find_one({"_id": account_id})
    accounts.update_one(
        {'_id': account_id},
        {"$set": {"IsDeleted": DeletedType.DELETED.value}
    })      
    flash(messages_success['delete_success'].format(account["Username"]), 'success')    
    return redirect('/admin/account')

@admin_blueprint.route('/admin/edit_account', methods=['POST'])
@login_required
def edit_account():
    try:
        log_in_id = session.get("account_id")
        account_id = request.form.get("account_id")
        id = ObjectId(account_id)
        role = roles.find_one({"Value": int(request.form['role'])}, {"_id":0})

        lst_login_method_type = list(map(int, request.form.getlist("loginMethod")))
        lst_transfer_method_type = list(map(int, request.form.getlist("transferMethod")))

        status = int(request.form.get("status"))

        lst_login_methods = list(login_methods.find(
            {'Value': {'$in': lst_login_method_type}}, 
            {'_id': 0}  
        ))

        lst_transfer_methods = list(transfer_methods.find(
            {'Value': {'$in': lst_transfer_method_type}}, 
            {'_id': 0}  
        ))

        request_branch = branches.find_one({"BranchName": request.form['branch']}, {"_id": 0})

        accounts.update_one(
            {'_id': id},
            {"$set": {
                "Role": role,
                "LoginMethod": lst_login_methods,
                "TransferMethod": lst_transfer_methods,
                "Branch": request_branch,
                "IsDeleted": status,
                "ModifiedBy": log_in_id
            }}
        )

        flash(messages_success["update_success"].format("Account"), 'success')
    except Exception:
        flash(messages_failure['internal_error'], 'error')
    return redirect("/admin/account")

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
    file = request.files['file']
    ext = get_file_extension(file.filename)

    if ext == FileType.CSV.value:
        df = pd.read_csv(BytesIO(file.read()))
    elif ext == FileType.XLSX.value:
        df = pd.read_excel(BytesIO(file.read()), engine='openpyxl')
        
    data = df.to_dict(orient='records')
    res = None

    if data_type == DataType.ACCOUNT.value:
        res = create_accounts(data)
    elif data_type == DataType.BRANCH.value:
        pass
    elif data_type == DataType.USER.value:
        pass
    elif data_type == DataType.EMPLOYEE.value:
        pass
    elif data_type == DataType.NEWS.value:
        pass
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
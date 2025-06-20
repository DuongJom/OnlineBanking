from models.database import Database
from enums.collection import CollectionType

db = Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
bills = db[CollectionType.BILLS.value]
branches = db[CollectionType.BRANCHES.value]
cards = db[CollectionType.CARDS.value]
card_types = db[CollectionType.CARD_TYPES.value]
employees = db[CollectionType.EMPLOYEES.value]
investments = db[CollectionType.INVESTMENTS_SAVINGS.value]
loans = db[CollectionType.LOANS.value]
login_methods = db[CollectionType.LOGIN_METHODS.value]
news = db[CollectionType.NEWS.value]
salaries = db[CollectionType.SALARIES.value]
roles = db[CollectionType.ROLES.value]
transfer_methods = db[CollectionType.TRANSFER_METHODS.value]
transactions = db[CollectionType.TRANSACTIONS.value]
users = db[CollectionType.USERS.value]
working_day_infos = db[CollectionType.WORKING_DAY_INFOS.value]
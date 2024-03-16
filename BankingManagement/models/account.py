from datetime import datetime
from  werkzeug.security import generate_password_hash

class Account:
    def __init__(self,  AccountNumber, Branch, AccountOwner, Username, Password, LoginMethod, TransferMethod, Serice,CreatedBy, ModifiedDate, ModifiedBy):
       self.AccountNumber = AccountNumber
       self.Branch = Branch
       self.AccountOwner = AccountOwner
       self.Username = Username
       self.Password = generate_password_hash(Password)
       self.LoginMethod = LoginMethod or []
       self.TransferMethod = TransferMethod or []
       self.Service = Serice or []
       self.CreatedDate = datetime.utcnow()
       self.CreatedBy = None
       self.ModifiedDate = None
       self.ModifiedBy = None



    def to_json(self):
        return {
            "AccountId" : self.AccountId,
            "AccountNumber" :  self.AccountNumber,
            "Branch" : self.Branch,
            "AccountOwner" : self.AccountOwner,
            "Username" : self.Username,
            "Password" : self.Password,
        }
    



    # - Account:
	# + AccountId: ObjectId
	# + AccountNumber: string
	# + Branch: Branch
	# + AccountOwner: User
	# + Username: string
	# + Password: string
	# + LoginMethod: LoginMethod[]
	# + TransferMethod: TransferMethod[]
	# + Service: Service[]
	# + CreatedDate: datetime
	# + CreatedBy: User
	# + ModifiedDate: datetime
	# + ModifiedBy: User
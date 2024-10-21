export const tableStructure = {
  account: [
    { key: "Username", name: "Username", isObject: false},
    { key: "AccountNumber", name: "Account Number", isObject: false },
    { key: "Branch", name: "Branch", isObject: false },
    { key: "AccountOwner", name: "Owner", object_key: "Name", isObject: true },
    { key: "Role", name: "Role", object_key: "RoleName", isObject: false },
    { key: "TransferMethod", name: "Transfer Method", object_key: "MethodName", isObject: true},
    { key: "LoginMethod", name: "Login Method", object_key: "MethodName", isObject: true}
  ],
  user: [
    { key: "Name", name: "Name", isObject: false },
    { key: "Sex", name: "Gender", isObject: false },
    { key: "Address", name: "Address", object_key: "District", isObject: false },
    { key: "Phone", name: "Phone", isObject: false },
    { key: "Email", name: "Email", isObject: false},
    { key: "Card", name: "Card", object_key: "CardNumber", isObject: true},
  ],
  branch: [
    { key: "BranchName", name: "Branch Name", isObject: false},
    { key: "Address", object_key: "District", name: "Address", isObject: true}
  ],
  employee: [
    { key: "EmployeeName", name: "Name", isObject: false },
    { key: "Position", name: "Position", isObject: false },
    { key: "Role", name: "Role", isObject: false},
    { key: "Sex", name: "Gender", isObject: false},
    { key: "Phone", name: "Phone", isObject: false},
    { key: "Email", name: "Email", isObject: false},
    { key: "Address", name: "Address", object_key: "Country", isObject: false},
    { key: "Check_in_time", name: "Check In", isObject: false},
    { key: "Check_out_time", name: "Check Out", isObject: false},
    { key: "Salary", name: "Salary", isObject: false},
  ],
  news: [
    { key: "Title", name: "Title", isObject: false},
    { key: "Content", name: "Content", isObject: false},
    { key: "StartDate", name: "Start date", isObject: false},
    { key: "EndDate", name: "End date", isObject: false},
    { key: "PublishedBy", name: "Publisher", isObject: false}
  ]
};

export const identifier = {
  account: "Username",
  user: "Name",
  branch: "BranchName",
  employee: "EmployeeName",
};

export const pages = {
  account: "Accounts",
  user: "Users",
  employee: "Employees",
  branch: "Branches",
}

export const filterType = {
  account: "accountFilterConditons",
  user: "userFilterConditions",
  employee: "employeeFilterConditions",
  branch: "branchFilterConditions"
}
export const tableStructure = {
  account: [
    { key: "Username", name: "Username" },
    { key: "AccountNumber", name: "Account Number" },
    { key: "Branch", name: "Branch" },
    { key: "AccountOwner", name: "Owner", object_key: "Name" },
    { key: "Role", name: "Role" },
    { key: "TransferMethod", name: "Transfer Method" },
    { key: "LoginMethod", name: "Login Method" }
  ],
  user: [
    { key: "Name", name: "Name" },
    { key: "Sex", name: "Gender" },
    { key: "Address", name: "Address" },
    { key: "Phone", name: "Phone" },
    { key: "Email", name: "Email" },
    { key: "Card", name: "Card", object_key: "CardNumber" },
  ],
  branch: [
    { key: "BranchName", name: "Branch Name" },
    { key: "Address", object_key: "District", name: "Address" }
  ],
  employee: [
    { key: "EmployeeName", name: "Name" },
    { key: "Position", name: "Position" },
    { key: "Role", name: "Role"},
    { key: "Sex", name: "Gender"},
    { key: "Phone", name: "Phone"},
    { key: "Email", name: "Email"},
    { key: "Address", name: "Address", object_key: "Country"},
    { key: "Check_in_time", name: "Check In"},
    { key: "Check_out_time", name: "Check Out"},
    { key: "Salary", name: "Salary"},
  ],
  news: [
    { key: "Title", name: "Title"},
    { key: "Content", name: "Content"},
    { key: "StartDate", name: "Start date"},
    { key: "EndDate", name: "End date"},
    { key: "PublishedBy", name: "Publisher"}
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
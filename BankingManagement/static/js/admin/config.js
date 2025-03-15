export const tableStructure = {
  account: [
    { name: "ID", isObject: false, isObjectId: true, isNumberFormat: false },
    { name: "Username", isObject: false, isObjectId: false, isNumberFormat: false },
    { name: "Account Number", isObject: false, isObjectId: false, isNumberFormat: false },
    { name: "Balance", isObject: false, isObjectId: false, isNumberFormat: true },
    { name: "Owner ID", isObject: false, isObjectId: true, isNumberFormat: false },
    { name: "Owner", isObject: true, isObjectId: false, isNumberFormat: false },
    { name: "Branch ID", isObject: false, isObjectId: true, isNumberFormat: false },
    { name: "Branch", isObject: true, isObjectId: false, isNumberFormat: false },
    { name: "Role", isObject: false, isObjectId: false, isNumberFormat: false },
    { name: "Transfer Method", isObject: false, isObjectId: false, isNumberFormat: false },
    { name: "Login Method", isObject: false, isObjectId: false, isNumberFormat: false }
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

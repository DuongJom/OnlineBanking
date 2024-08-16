export const table_structure = {
  account: [
    { key: "Username", name: "Username" },
    { key: "AccountNumber", name: "Account Number" },
    { key: "Branch", name: "Branch" },
    { key: "AccountOwner", object_key: "Name", name: "Owner" },
    { key: "Role", name: "Role" },
    { key: "TransferMethod", name: "Transfer Method" },
    { key: "LoginMethod", name: "Login Method" },
    { key: "Service", name: "Service" },
  ],
  user: [],
};

export const object_identifier = {
  account: "Username",
  user: "Name",
  branch: "BranchName",
  employee: "EmployeeName",
};

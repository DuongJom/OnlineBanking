export const table_structure = {
    account: [
        {key: 'Username', name: 'Username'}, 
        {key: 'AccountNumber', name: 'Account Number'}, 
        {key: 'Branch', name: 'Branch'}, 
        {key: "AccountOwner", name: 'Owner'}, 
        {key: 'Role', name: 'Role'}, 
        {key: 'TransferMethod', name: 'Transfer Method'}, 
        {key: 'LoginMethod', name: 'Login Method'}, 
        {key: 'Service', name: 'Service'}],
}

export const styles = {
    cell: 'whitespace-nowrap p-2 relative border-x border-black',
    table: 'border border-black',
    table1: 'border border-black z-10 sm:fixed shadow-shadowRight',
    table2: 'flex-1 border border-black',
    th: 'text-left p-2 border border-black whitespace-nowrap',
    tr: 'h-8 bg-blue-gray-50 my-3 border-t border-white',
    table_wrapper: 'w-99% flex absolute top-20 overflow-x-auto',
    thead: 'bg-blue-gray-300',
}
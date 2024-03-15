# Project for Online Banking
Dự án sử dụng các công nghệ sau:
- Back-end side: Flask, MongoDB
- Front-end: HTML, JavaScript, Tailwind CSS, JQuery
- Tham khảo cách config Tailwind CSS cho project: https://flowbite.com/docs/getting-started/flask/

<b>Chức năng của hệ thống:</b>
- Chức năng chung:
	+ Đăng nhập
	+ Đăng xuất
	+ Đăng ký
	+ Quên mật khẩu
	+ Thay đổi mật khẩu
	+ Thay đổi thông tin
	+ Xem thông tin cá nhân
- Người dùng:
	+ Chuyển/nạp tiền vào tài khoản
	+ Xem trạng thái tài khoản, trạng thái chuyển tiền
	+ Thanh toán hóa đơn điện, nước, Wi-Fi, cước di động, viện phí, học phí, vé máy bay, cước truyền hình cáp, dịch vụ chung cư
	+ Tra cứu/sao kê
	+ Gia hạn thẻ ghi nợ
	+ Phát hành/Chuyển đổi thẻ
	+ Thanh toán thẻ tín dụng
	+ Gửi tiết kiệm
- Nhân viên:
	+ Check-in
	+ Check-out
	+ Kiểm tra lương
	+ Đăng ký day-off/WFH
	+ Kiểm toán
	+ Sao kê
	+ Giao dịch
- Quản trị viên:
	+ Quản lý tài khoản
	+ Quản lý người dùng
	+ Quản lý nhân viên
	+ Quản lý chi nhánh/PGD

<b>Database:</b>
- Account:
	+ AccountId: ObjectId
	+ AccountNumber: string
	+ Branch: Branch
	+ AccountOwner: User
	+ Username: string
	+ Password: string
	+ LoginMethod: LoginMethod[]
	+ TransferMethod: TransferMethod[]
	+ Service: Service[]
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- User:
	+ UserId: ObjectId
	+ Name: string
	+ Sex: bit
	+ Address: string
	+ Phone: string
	+ Email: string
	+ CardID: string
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User

- Branch:
	+ BranchId: ObjectId
	+ BranchName: string
	+ Address: Address
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- Address:
	+ AddressId: ObjectId
	+ Street: string
	+ Ward: string
	+ District: string
	+ City: string
	+ Country: string
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- LoginMethod:
	+ MethodId: ObjectId
	+ MethodName: string
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- TransferMethod:
	+ MethodId: ObjectId
	+ MethodName: string
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- Service:
	+ ServiceId: ObjectId
	+ ServiceName: string
	+ Infomation: ServiceInfo[]
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- ServiceInfo:
	+ InfoId: ObjectId
	+ Content: string
	+ TotalAmount: double
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User

- Employee:
	+ EmployeeId: ObjectId
	+ EmployeeName: string
	+ Sex: bit
	+ Phone: string
	+ Email: string
	+ Address: Address
	+ Checkin_time: datetime
	+ Checkout_time: datetime
	+ Working_status: bit
	+ TotalDayOff: int
	+ DayOff: DayOffInfo[]
	+ Salary: double
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- DayOffInfo:
	+ InfoId: ObjectId
	+ Day: day
	+ Month: month
	+ Year: year
	+ DayOffType: Type
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- Type:
	+ TypeId: ObjectId
	+ TypeName: string
	+ TypeValue: double
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User
	
- Card:
	+ CardId: ObjectId
	+ CardNumber: string
	+ ExpiredDate: datetime
	+ IssuanceDate: datetime
	+ Type: CardType[]
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User

- CardType:
	+ TypeId: ObjectId
	+ TypeName
	+ CreatedDate: datetime
	+ CreatedBy: User
	+ ModifiedDate: datetime
	+ ModifiedBy: User

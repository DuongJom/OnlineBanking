# 💳 Online Banking Website

A modern, secure, and scalable online banking system built with **Flask (Python)** for the backend, **MongoDB** for database management, and a responsive UI using **Tailwind CSS, HTML, JavaScript, and jQuery**.

---

## 🚀 Technologies Used

### 🧠 Back-End

* [Flask](https://flask.palletsprojects.com/) - Lightweight Python web framework
* [MongoDB](https://www.mongodb.com/) - NoSQL document-based database
* [PyMongo](https://pymongo.readthedocs.io/) - MongoDB driver for Python
* [Flask Blueprint](https://flask.palletsprojects.com/en/latest/blueprints/) - Modular architecture

### 🎨 Front-End

* [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
* [jQuery](https://jquery.com/)

---

## 📦 Project Structure

```
BankingManagement/
│
├── app.py                 # Entry point
├── .env                   # Environment variables
├── db.py                  # MongoDB shared instance
├── requirements.txt       # Python dependencies
│
├── templates/             # HTML templates
│   ├── general/
│   ├── user/
│   ├── admin/
│   └── employee/
│
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── img/
│
├── blueprints/               # Flask Blueprints (account, user, admin...)
│   ├── user/
│   ├── employee/
│   └── admin/
│
└── ...
```

---

## 🧐 Features

### 🔐 Common

* User Authentication (Login, Logout, Register, Forgot Password, Change Password)
* View and Update Profile

### 👤 For Users

* Transfer & Deposit Money
* Account and Transaction Status
* Pay Bills: Electricity, Water, Wi-Fi, Phone, Hospital, Tuition, Flight, Cable TV, Condo Services
* Statement/History Lookup
* Debit Card Renewal & Conversion
* Credit Card Payment
* Savings Management

### 👨‍💼 For Employees

* Check-in / Check-out
* View Salary
* Request Day-off / Work-from-home
* Auditing & Transaction Management

### 🛠 For Admins

* Manage Users & Employees
* Manage Branches
* Account Management

---

## 🗃️ Database Schema

The system uses MongoDB collections such as:

* `Account`, `User`, `Branch`, `Card`, `Employee`
* Lookup collections: `LoginMethod`, `TransferMethod`, `CardType`, `Service`, `Type`, etc.
* Embedded sub-documents: `Address`, `ServiceInfo`, `DayOffInfo`

Each document includes:

* `created_date`, `created_by`, `modified_date`, `modified_by` for audit tracking

---

## 🛠️ Setup Instructions

### 📦 Prerequisites

* Python 3.11+
* MongoDB running locally or via MongoDB Atlas
* Node.js & npm (for Tailwind CSS compilation, optional)

### 📅 Clone Project

```bash
git clone https://github.com/DuongJom/OnlineBanking.git
cd OnlineBanking
```

### 🔐 Create `.env` file

```env
MONGODB_URI=mongodb://localhost:27017
DB_NAME=OnlineBanking
SECRET_KEY=your-secret-key
```

### 📥 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 🎨 Tailwind CSS Setup (optional)

> Following [Flowbite Tailwind setup for Flask](https://flowbite.com/docs/getting-started/flask/)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

Configure `tailwind.config.js`, then run:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
```

---

## ▶️ Run the App

```bash
python app.py
```

App runs at: [http://localhost:5000](http://localhost:5000)

---

## 🔒 Security Notes

* Passwords are securely hashed.
* MongoDB injection prevented via PyMongo query binding.
* Form inputs validated both client-side and server-side.

---

## 📸 Screenshots

> Add screenshots of UI (login page, dashboard, etc.)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Credits

* Built by Duong Nguyen and contributors.
* UI inspired by [Flowbite](https://flowbite.com/) + Tailwind CSS

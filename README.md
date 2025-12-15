# 🔐 Cybersecurity Login System

A GUI-based cybersecurity mini project developed using **Python and wxPython**.  
This project demonstrates **basic cybersecurity concepts** such as password hashing, login attempt monitoring, account locking, and admin monitoring.

---


## 📌 Features

### 👤 User Features
- User registration with username uniqueness check
- Password strength checker with live progress bar
- Warning popup for weak/medium passwords
- Secure password storage using **SHA-256 hashing**
- Login system with limited attempts
- Temporary account lock after multiple failed logins
- Countdown timer showing lock duration

### 👮 Admin Features
- Protected admin login
- Admin dashboard to view login logs
- Monitoring of failed and successful login attempts
- Read-only access (no user manipulation)

---

## 🧠 Cybersecurity Concepts Used
- Password hashing (SHA-256)
- Prevention of brute-force attacks
- Suspicious login detection
- Secure credential storage
- Role-based access (User / Admin)

---

## 🛠️ Technologies Used
- **Python 3**
- **wxPython** (GUI)
- Standard Python libraries:
  - `hashlib`
  - `datetime`
  - `time`
  - `os`

---

## 📂 Project Structure

Cybersecurity-Login-System
```text
├── main.py          # The core application logic and UI code
├── users            # (or users.txt) Stores username and hashed passwords
├── login_logs       # (or login_logs.txt) Stores audit trail of login attempts
├── admin            # (or admin.ico) Icon file for Admin windows
└── app              # (or app.ico) Icon file for the Main application
```
---

## 🖼️ Screenshots

Below are some screenshots demonstrating the working of the Cybersecurity Login System.

### 🔐 Login Screen
- Username & password input
- Shows remaining login attempts
- Link to signup page
- Admin login access

<img width="629" height="658" alt="Screenshot 2025-12-15 201251" src="https://github.com/user-attachments/assets/7208eebd-3e58-40bf-9144-ce641aeb595b" />

---
### 🚫 Account Lock Mechanism
- Account temporarily locked after multiple failed login attempts
- Countdown timer displayed to user

<img width="626" height="654" alt="image" src="https://github.com/user-attachments/assets/28107b92-80da-4309-87fa-5447d9651ab9" />

---

### 📝 Signup Screen
- User registration interface
- Username availability check
- Password strength meter (Weak / Medium / Strong)
- Warning popup for weak passwords

<img width="625" height="662" alt="image" src="https://github.com/user-attachments/assets/807c0935-1a59-4b24-9e22-29f84d90ecee" />

<img width="628" height="657" alt="image" src="https://github.com/user-attachments/assets/301d7c1f-5443-4307-b265-42c936619791" />



---


### 👮 Admin Login
- Secure admin authentication screen

<img width="351" height="259" alt="image" src="https://github.com/user-attachments/assets/e34a4754-809f-4179-b720-d8f7232782a0" />

--- 

### 📊 Admin Panel
- Displays login attempt logs with timestamps
- Helps monitor suspicious login activity

<img width="719" height="543" alt="image" src="https://github.com/user-attachments/assets/44844442-8ba9-4df0-98a7-39e2adc7cc90" />



## ▶️ How to Run

### 1. Install wxPython
```bash
pip install wxpython
```
### 2. Run the application
```bash
python main.py
```
### 3. Admin Login Credentials
```bash
Username: admin
Password: admin123
```
- These credentials are for demonstration purposes.





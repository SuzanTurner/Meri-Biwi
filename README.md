# 💍 Meri Didi Backend API

A FastAPI backend for **Meri Didi**, a service-based application designed to handle user and worker data efficiently.  
Built with **FastAPI**, **SQLAlchemy**, and **MySQL**, and sprinkled with just the right amount of backend badassery.  

---

## 🚀 Features

- User CRUD operations
- MySQL database integration
- SQLAlchemy ORM with models
- Clean RESTful API routes
- Indian Standard Time (IST) timestamps
- Optional form field handling
- Secure password + UID generation
- Fully async & production-ready 🍃

---

## 🛠️ Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **Uvicorn** (for local dev server)
- **Pydantic**
- **dotenv**
- **pytz** (for timezone handling)

---

## 📁 Project Structure
`
backend-app/
├── main.py
├── database.py
├── models/
│ └── user.py
├── routers/
│ └── users.py
├── schemas/
│ └── user.py
├── .env
├── requirements.txt
`

## 🧪 Setup & Run (Local)

### 1. Clone the repo

```bash
git clone https://github.com/SuzanTurner/Meri-Biwi/backend-app.git
```

### 2. Set up virtual environment
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 4. Configure your .env file
### 5. Run the app
```
uvicorn main:app --reload
 ```

## API Endpoints

| Method | Route         | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/users/{id}` | Get user by ID      |
| POST   | `/users/`     | Create a new user   |
| PUT    | `/users/{id}` | Update user by ID   |
| DELETE | `/users/{id}` | Delete user by ID   |
| GET    | `/users`   | Get all Users |

## 🌍 Timezone
All timestamps (created_at, updated_at) are stored in Indian Standard Time (Asia/Kolkata) using pytz.

## 🧠 UID Generation
User UID is a random alphanumeric string generated using Python's uuid or secrets library — guaranteed unique, like your code.


I deserve a Cold Coffee
- The_CrUd_LaDy


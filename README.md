# 🧹 Meri-Didi – Backend API

This is the backend for the [**Meri-Didi**](https://meri-didi.vercel.app) website — a platform that helps you find trustworthy domestic helpers, without the drama. Built with FastAPI and PostgreSQL, it's lightweight, clean, and built to just *work*.

## 🛠️ Stack Breakdown

- **Backend**: FastAPI (clean, fast, and async-ready)  
- **Database**: PostgreSQL  
- **Hosting**: Both backend and database are deployed on **Render**  
- **Frontend**: The official Meri-Didi website lives on **Vercel**  
- **Author**: Yadhnika Wakde (ThE_CrUd_LaDy 😎) and Ritesh Singh

## 🌐 API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
`register-worker.py `
| POST   | `/register-worker`| Register a new worker              |
| GET    | `/search-workers` | Search registered workers by name  |
| GET    | `/all`            | Get all workers                    |  
`update.py`
| PUT    | `/update/{id}`     | Update worker status and religion by ID         |
`db_check.py`
| GET    | `/db_check`       | For checking db connection (Devs only) |
`service.py`
| POST | `/services` | Create a service |
| GET | `/services` | Get all serivces |
| GET | `/services/{id}` | Get services by id |
| PUT | `/services/{id}` | Update service by id |
`user.py`
| POST | `/create-user` | Create a new user | 
| GET | `/create-user/{id}` | Get a user by id |
`login.py`
| POST | `/login` | Log in user through username and password |



Please See /docs endpoint for More info

## 💾 Database Setup

There are **two database instances**:  
- One for **local dev**  
- One that's **live on Render**  

*Only I get access for the actual site*

## 🧪 Running Locally

1. Clone this repo  
2. Install the goods:  
   ```bash
   pip install -r requirements.txt
   ```
3. Add your .env file with:
```
DATABASE_URL=your_local_or_render_db_url
```
4. Run:
```terminal
uvicorn main:app --reload
```

## ⚡ Quick Note
Clicking the "Register Worker" button on the frontend sends data here — and we faithfully toss it into the database like it's the holy grail. You can also search workers by name if you're tryna locate someone specific.


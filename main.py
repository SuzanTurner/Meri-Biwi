from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import uvicorn
from routers import db_check, login, service, testimonials, users, admin, otp, categories, workers

app = FastAPI(debug = True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(workers.router)
app.include_router(db_check.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(service.router)
app.include_router(admin.router)
app.include_router(otp.router)
app.include_router(categories.router)
app.include_router(testimonials.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)



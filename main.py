from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import banners, db_check, login, service, testimonials, users, admin, otp, categories, cooking, cleaning, preference, bookings, areas, attendance, notifications, phonepay, new_workers, ratings
import uvicorn
import logging


logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(debug = True)

app.mount("/uploads-workers", StaticFiles(directory="uploads-workers"), name="uploads-workers")
app.mount("/uploads-admin", StaticFiles(directory="uploads-admin"), name="uploads-admin")
app.mount("/uploads-categories", StaticFiles(directory="uploads-categories"), name="uploads-categories")
app.mount("/uploads-testimonials", StaticFiles(directory="uploads-testimonials"), name="uploads-testimonials")
app.mount("/uploads-banners", StaticFiles(directory="uploads-banners"), name="uploads-banners")
app.mount("/uploads-users", StaticFiles(directory="uploads-users"), name = "uploads-users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

# app.include_router(workers.router)
app.include_router(db_check.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(service.router)
app.include_router(admin.router)
app.include_router(otp.router)
app.include_router(categories.router)
app.include_router(testimonials.router)
app.include_router(cooking.router)
app.include_router(cleaning.router)
app.include_router(banners.router)
app.include_router(preference.router)
app.include_router(bookings.router)
app.include_router(areas.router)
app.include_router(attendance.router)
app.include_router(notifications.router)
app.include_router(phonepay.router)
app.include_router(new_workers.router)
app.include_router(ratings.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)



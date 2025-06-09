from fastapi import FastAPI, APIRouter
from database import Base, engine
from routers import users, login
import uvicorn

app = FastAPI(debug = True)

Base.metadata.create_all(bind=engine)

routers = APIRouter()

app.include_router(users.router)
app.include_router(login.router)


if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000)
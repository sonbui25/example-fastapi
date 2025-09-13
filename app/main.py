from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
app = FastAPI()

# models.Base.metadata.create_all(bind=engine) # Lệnh này sẽ tạo tất cả các bảng trong cơ sở dữ liệu chỉ khi không xài alembic

origins = ["https://www.google.com"] # Danh sách các domain được phép gửi request đến API của bạn, có thể là ["*"] để cho phép tất cả các domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router) 
app.include_router(vote.router)

@app.get("/")
def root(): 
    return {"message": "Hello World!!!"}


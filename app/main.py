from fastapi import FastAPI
from . import models,schemas,utils
from .database import engine
from .routers import post,user, auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)   #don't need it as we will be using Alembic as data nigration tool
app=FastAPI()
origins=["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def root():
    return{"message": "Welcome VJ FASTAPI WORLD!!"}







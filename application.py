import uvicorn
from fastapi import FastAPI

from blog.routers import blog, user
from blog import modals
from blog.database import engine

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)


# create database modals 
modals.Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
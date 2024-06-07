from fastapi import FastAPI
from app.routers import users

app = FastAPI()

@app.get('/')
async def root():
    return "E ai rapeize"


app.include_router(users.router)
# app.include_router(users.test_router)
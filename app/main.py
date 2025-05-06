from fastapi import FastAPI
from app.interfaces.routes import products

app = FastAPI()
app.include_router(products.router)
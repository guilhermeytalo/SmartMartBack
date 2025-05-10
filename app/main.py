from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.routes import category, products

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products.router)
app.include_router(category.router)

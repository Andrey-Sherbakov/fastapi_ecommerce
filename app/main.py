from fastapi import FastAPI

from app.middleware import log_middleware
from app.routers import category, products, auth, permissions, review

app = FastAPI(swagger_ui_parameters={'persistAuthorization': True})

app.middleware('http')(log_middleware)


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permissions.router)
app.include_router(review.router)

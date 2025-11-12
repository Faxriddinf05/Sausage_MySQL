from fastapi import FastAPI
from routers.users import user_router
from routers.login import login_router
from fastapi.middleware.cors import CORSMiddleware
from routers.products import product_router
from routers.orders import order_router
from routers.order_items import order_item_router


app = FastAPI(docs_url="/", title="Sausage Factory API on MySQL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(order_item_router, tags=["Buyurtma elementlari"])
app.include_router(order_router, tags=["Buyurtma"])
app.include_router(user_router, tags=["Profil"])
app.include_router(login_router)
app.include_router(product_router, tags=["Mahsulotlar"])

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import Base, engine, get_db
from routers.users import user_router, admin_router
from routers.login import login_router
from fastapi.middleware.cors import CORSMiddleware
from routers.products import product_router
from routers.orders import order_router
from routers.order_items import order_item_router
import models


app = FastAPI(docs_url="/", title="Sausage Factory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT 1")
    return {"db_status": result.scalar()}

app.include_router(order_item_router, tags=["Buyurtma elementlari"])
app.include_router(order_router, tags=["Buyurtma"])
app.include_router(user_router, tags=["Profil"])
app.include_router(admin_router, tags=["Admin"])
app.include_router(login_router)
app.include_router(product_router, tags=["Mahsulotlar"])

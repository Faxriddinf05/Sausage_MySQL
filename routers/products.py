from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models.products import Products
from schemas.products import SchemaProducts
from sqlalchemy.future import select
from sqlalchemy import update, delete
from datetime import datetime, timedelta
from models.order_items import OrderItem
from models.orders import Order
import os

product_router = APIRouter()


# Barcha mahsulotlarni ko'rish uchun API
@product_router.get("/Mahsulotlarni_ko'rish")   # barcha ma'lumotlarni ko'rish
async def get_all(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Products))
    return result.scalars().all()


# Mahsulotlarni tartibi ya'ni ID bo'yicha ko'rish uchun API
@product_router.get("/Mahsulotlarni_id_bilan_ko'rish")
async def get_product(ident:int = None, db:AsyncSession = Depends(get_db)):
    if ident:
        a = await db.execute(select(Products).where(Products.id == ident))
        return a.scalar()
    else:
        a = await db.execute(select(Products))
        return a.scalars().all()


@product_router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    try:
        # 1. Остаток продуктов
        result = await db.execute(select(Products))
        products = result.scalars().all()
        stock = {p.name: p.quantity for p in products}

        # 2. Общие продажи
        result = await db.execute(select(OrderItem.quantity))
        total_sold = sum([item[0] for item in result.all()])

        # 3. Продажи за неделю
        week_ago = datetime.now() - timedelta(days=7)
        result = await db.execute(
            select(OrderItem.quantity)
            .join(Order)
            .filter(Order.created_at >= week_ago)
        )
        sold_week = sum([item[0] for item in result.all()])

        # 4. Продажи за месяц
        month_ago = datetime.now() - timedelta(days=30)
        result = await db.execute(
            select(OrderItem.quantity)
            .join(Order)
            .filter(Order.created_at >= month_ago)
        )
        sold_month = sum([item[0] for item in result.all()])

        return {
            "остатки всех продуктов": stock,
            "суммарно сколько всего продано": total_sold,
            "сколько продано за последние 7 дней": sold_week,
            "сколько продано за последние 30 дней": sold_month
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







# 1️⃣ Остатки продуктов
@product_router.get("/stock")
async def get_stock(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Products))
        products = result.scalars().all()
        stock = {p.name: p.quantity for p in products}
        return {"stock": stock}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2️⃣ Общие продажи
@product_router.get("/total-sold")
async def get_total_sold(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderItem.quantity))
        total_sold = sum([item[0] for item in result.all()])
        return {"total_sold": total_sold}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 3️⃣ Продажи за неделю
@product_router.get("/week")
async def get_week_sales(db: AsyncSession = Depends(get_db)):
    try:
        week_ago = datetime.now() - timedelta(days=7)
        result = await db.execute(
            select(OrderItem.quantity)
            .join(Order)
            .filter(Order.created_at >= week_ago)
        )
        sold_week = sum([item[0] for item in result.all()])
        return {"sold_last_week": sold_week}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 4️⃣ Продажи за месяц
@product_router.get("/month")
async def get_month_sales(db: AsyncSession = Depends(get_db)):
    try:
        month_ago = datetime.now() - timedelta(days=30)
        result = await db.execute(
            select(OrderItem.quantity)
            .join(Order)
            .filter(Order.created_at >= month_ago)
        )
        sold_month = sum([item[0] for item in result.all()])
        return {"sold_last_month": sold_month}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







# Mahsulot qo'shish uchun API
@product_router.post("/Mahsulot_qo'shish")
async def add_product(form:SchemaProducts, db:AsyncSession = Depends(get_db)):
    product = Products(
        name = form.name,
        heading = form.heading,
        price = form.price,
        amount = form.amount,
        image = form.image
    )
    db.add(product)
    await db.commit()
    return "Mahsulot bazaga qo'shildi !"



UPLOAD_DIR = "images"  # папка для изображений
os.makedirs(UPLOAD_DIR, exist_ok=True)



# Mahsulotga rasm yuklash uchun API (Bu hozircha yopilgan, agar zarurat bo'lsa ishlatib beriladi)

@product_router.post("/{product_id}/rasm-yuklash")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        # Проверяем, существует ли продукт
        result = await db.execute(select(Products).filter(Products.id == product_id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")

        # Проверка типа файла
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Можно загружать только изображения")

        # Генерация уникального имени файла
        filename = f"product_{product_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Сохраняем файл
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Сохраняем путь в базе
        product.image = f"/{file_path}"  # например: /static/products/product_1_image.jpg
        await db.commit()

        return {"message": "Изображение успешно добавлено", "image_url": product.image}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mahsulotni tahrirlash (o'zgartirish) uchun API
@product_router.put("/Mahsulot_tahrirlash")
async def update_product(ident: int, form:SchemaProducts, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Products).where(Products.id == ident))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found !")

    await db.execute(update(Products).where(Products.id == ident).values(
        name=form.name,
        heading=form.heading,
        price=form.price,
        amount=form.amount,
        image=form.image
    ))
    await db.commit()
    return "Mahsulot tahrirlandi !"


# Mahsulotni o'chirib yuborish uchun API
@product_router.delete("/Mahsulot_o'chirish")
async def delete_product(ident: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Products).where(Products.id == ident))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found !")

    await db.execute(delete(Products).where(Products.id == ident))
    await db.commit()
    return "Mahsulot o'chirildi !"



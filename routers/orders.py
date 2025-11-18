from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from db import get_db
from models.orders import Order
from models.order_items import OrderItem
from models.products import Products
from schemas.orders import SchemaOrder, SchemaOrderItem

order_router = APIRouter()


# Barcha buyurtmalarni ko'rish uchun API
@order_router.get("/Buyurtmalarni_ko'rish")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()


# Bitta buyurtmani ID orqali ko'rish uchun API
@order_router.get("/Buyurtmani_id_bilan_ko'rish")
async def get_order(ident: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == ident))
    order = result.scalar()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi !")
    return order


# Buyurtma yaratish (Order + Order_item) uchun API
@order_router.post("/Buyurtma_yaratish")
async def create_order(form: SchemaOrder, db: AsyncSession = Depends(get_db)):
    """
    SchemaOrder tarkibi:
    {
        "user_id": 1,
        "address": "Farg'ona, Al-Farg'oniy 10",
        "items": [
            {"product_id": 2, "amount": 3},
            {"product_id": 5, "amount": 1}
        ]
    }
    """
    total_price = 0
    order_items_list = []

    for item in form.items:
        result = await db.execute(select(Products).where(Products.id == item.product_id))
        product = result.scalar()

        if not product:
            raise HTTPException(status_code=404, detail=f"Mahsulot ID {item.product_id} topilmadi")

        if product.amount < item.amount:
            raise HTTPException(status_code=400, detail=f"{product.name} mahsulotidan yetarli emas")

        price = product.price * item.amount
        total_price += price

        # Mahsulot miqdorini kamaytirish
        await db.execute(
            update(Products)
            .where(Products.id == item.product_id)
            .values(amount=product.amount - item.amount)
        )

        order_items = OrderItem(
            product_id=item.product_id,
            amount=item.amount,
            price=price
        )
        order_items_list.append(order_items)

    new_order = Order(
        user_id=form.user_id,
        address=form.address,
        total_price=total_price,
        status="Kutilmoqda",
        order_items=order_items_list
    )

    db.add(new_order)
    await db.commit()
    return {"xabar": "Buyurtma muvaffaqiyatli yaratildi", "buyurtma_id": new_order.id}


# Buyurtma statusini o'zgartirish (uchun API)
@order_router.put("/Buyurtma_statusini_o'zgartirish")
async def update_order_status(ident: int, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == ident))
    order = result.scalar()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi !")

    await db.execute(update(Order).where(Order.id == ident).values(status=status))
    await db.commit()
    return "Buyurtma statusi o'zgartirildi !"


# Buyurtmani o'chirish uchun API
@order_router.delete("/Buyurtmani_o'chirish")
async def delete_order(ident: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == ident))
    order = result.scalar()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi !")

    await db.execute(delete(Order).where(Order.id == ident))
    await db.commit()
    return "Buyurtma o'chirildi !"

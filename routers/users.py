from functions.users import get_own, sign_up, update_self, user_image, delete_self, add_user, add_admin
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from models.users import Users
from routers.login import get_current_user
from schemas.users import UserSch
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.users import UserSch


user_router = APIRouter()
admin_router = APIRouter()

# # Barchani ko'rish
# @admin_router.get('/get_users')
# async def barchani_korish(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Users))
#     return result.scalars().all()


# # Foydalanuvchi qo'shish - Ochiq
# @user_router.post('/add_user')
# async def add_user_open(form:UserSch, db: AsyncSession = Depends(get_db)):
#     try:
#         return await add_user(form, db)
#     except Exception as e:
#         raise e
#     except HTTPException as e:
#         raise HTTPException(status_code=400, detail=str(e))

# O'zini ko'rish uchun API
@user_router.get('/get_own_lock')
async def ozini_korish(db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    """
    Ro'yhatdan o'tgan foydalanuvchi o'zi haqidagi ma'lumotlarni ko'radi
    :param db:
    :param current_user:
    :return:
    """
    return await get_own(db, current_user)


# Barchani ko'rish uchun API (Adminga hos ish)
@admin_router.get('/get_users_lock')
async def foydalanuvchilarni_korish(db:AsyncSession=Depends(get_db), current_user: Users = Depends(get_current_user)):
    result = await db.execute(select(Users))
    try:
        return result.scalars().all()
    except Exception as h:
        raise (HTTPException(400, str(h)))


# Foydalanuvchi qo'shish uchun API, hamda ro'yxatdan o'tish
@admin_router.post('/post_users')
async def foydalanuvchi_qoshish(form:UserSch, db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
    try:
        return await sign_up(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


# # qulfsiz foydalanuvchi qo'shish routeri (zarur bo'lsa ishlatib beriladi)
# @user_router.post('/post_users')
# async def foydalanuvchi_qoshish(form:UserSch, db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
#     try:
#         return await sign_up(form, db, current_user)
#     except Exception as e:
#         raise HTTPException(400, str(e))



@admin_router.post('/post_admin')
async def admin_qoshish(form:UserSch, db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
    try:
        return await add_admin(form, db, current_user)
    except Exception as f:
        raise HTTPException(400, str(f))


# o'zini tahrirlash uchun API (o'zi haqidagi ma'lumotlarni o'zgartirish)
@admin_router.put('/put_own')
async def ozini_tahrirlash(form:UserSch, db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
    try:
        return await update_self(form, db, current_user)
    except Exception as d:
        raise HTTPException(400, str(d))


# o'ziga rasm yuklash uchun API
@admin_router.post('/load_image')
async def oziga_rasm_yuklash(file:UploadFile, db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
    try:
        return await user_image(file, db, current_user)
    except Exception as i:
        raise HTTPException(400, str(i))



# o'zini o'chirish uchun API (o'zini tizimdan chiqarib yuborish)
@admin_router.delete('/delete_self')
async def ozini_ochirish(db:AsyncSession = Depends(get_db), current_user : Users = Depends(get_current_user)):
    try:
        return await delete_self(db, current_user)
    except Exception as j:
        raise HTTPException(400, str(j))


# # shifrlanmagan parolni shifrlash
# @user_router.put('/hash_password')
# async def shifr_parol(ident:int, form:UserSch, db:AsyncSession=Depends(get_db)):
#     return await hash_old_user(ident, form, db)
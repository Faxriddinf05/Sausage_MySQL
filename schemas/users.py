from pydantic import BaseModel, Field, EmailStr

class UserSch(BaseModel):
    name : str
    email : EmailStr
    password : str = Field(..., min_length=8, description="Parol kamida 8 ta belgidan iborat bo'lishi kerak ! ")
    phone_number : str

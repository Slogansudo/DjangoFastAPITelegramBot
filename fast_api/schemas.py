from pydantic import BaseModel
from typing import Optional
from datetime import timedelta


class StatusModel(BaseModel):
    name: str


class OurTeamModel(BaseModel):
    employee_id: int
    photo: Optional[str]
    status_id: int


class CommentModel(BaseModel):
    text: str
    customer: str


class CategoryModel(BaseModel):
    title: str
    products_count: int
    photo: Optional[str]


class ProductModel(BaseModel):
    title = str
    description: str
    manufacturer_name: str
    discount: Optional[float]
    image: str
    price: float
    category_id: int
    comment: CommentModel


class RegisterModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True,
        schema_extra = {
            "id": 1,
            "first_name": "John",
            "last_name": "Smith",
            "username": "Smith",
            "email": "example@gmail.com",
            "password": "*****",
            "is_staff": True,
            "is_active": True
        }


class LoginModel(BaseModel):
    username: str
    password: str


class JwtModel(BaseModel):
    authjwt_secret_key: str = '6379e4ca89e82bf7864bed67bb305144bd0ae55e4f78d48672a2b5b7dee82244'
    authjwt_access_token_expires: timedelta = timedelta(minutes=20)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)


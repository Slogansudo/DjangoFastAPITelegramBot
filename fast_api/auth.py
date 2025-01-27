
from fastapi import APIRouter
from httpx import Auth
from schemas import RegisterModel, LoginModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Users
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/users")
async def get_users(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        data1 = session.query(Users).all()
        data = []
        for i in data1:
            form = {
                    'username': i.username,
                    'email': i.email,
                    'password': '*****',
                    'is_staff': i.is_staff,
                    'is_active': i.is_active,
                    'is_superuser': i.is_superuser
            }
            data.append(form)
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")




@auth_router.delete("/users/{id}")
async def delete_user(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        user = session.query(Users).filter(Users.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            session.delete(user)
            session.commit()
            return HTTPException(status_code=status.HTTP_508_LOOP_DETECTED, detail="user successfully deleted")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@auth_router.get("/")
async def auth():
    return {"message": "THIS IS THE AUTH PAGE"}


@auth_router.get("/login")
async def login():
    return {"message": "THIS IS LOGIN PAGE"}


@auth_router.post("/login")
async def new_login(request_user: LoginModel, Authorization: AuthJWT = Depends()):
    user = session.query(Users).filter(Users.username == request_user.username).first()
    if user:
        access_token = Authorization.create_access_token(subject=user.username)
        refresh_token = Authorization.create_refresh_token(subject=user.username)
        data = {
            "code": 200,
            "message": "login successful",
            "user": {
                "username": user.username
            },
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bunday foydalanuvchi topilmadi")


@auth_router.get('/register')
async def register():
    return {'message': 'welcome to Register page '}


@auth_router.post('/register')
async def new_register(user: RegisterModel):
    username = session.query(Users).filter(Users.username == user.username).first()
    if username:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday foydalanuvchi allaqachon mavjud")
    email = session.query(Users).filter(Users.email == user.email).first()

    if email:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday bunday email allaqachon mavjud")

    new_user = Users(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(new_user)
    session.commit()
    data = {'username': new_user.username, 'email': new_user.email, "is_active": new_user.is_active}
    return HTTPException(status_code=status.HTTP_201_CREATED, detail=data)


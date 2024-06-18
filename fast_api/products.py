from fastapi import APIRouter
from schemas import ProductModel, CommentModel, CategoryModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Comments, Product, Users, Category
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

product_router = APIRouter(prefix='/products')
session = Session(bind=ENGINE)


@product_router.get('/')
async def get_products(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    products = session.query(Product).all()
    return products


@product_router.post('/create')
async def create_product(productmodel: ProductModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    category = session.query(Category).filter(Category.id == productmodel.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
    user = session.query(Users).filter(Users.username == productmodel.comment.customer).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the user does not exist")
    new_comment = Comments(
        text=productmodel.comment.text,
        customer_id=user.id
    )
    session.add(new_comment)
    session.commit()
    new_product = Product(
        title=productmodel.title,
        description=productmodel.description,
        manufacturer_name=productmodel.manufacturer_name,
        discount=productmodel.discount,
        image=productmodel.image,
        price=productmodel.price,
        category_id=productmodel.category_id,
        comments_id=new_comment.id
    )
    session.add(new_product)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="The product successfully created!")

@product_router.get("/category")
async def get_categories(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    categories = session.query(Category).all()
    return HTTPException(status_code=status.HTTP_200_OK, detail=categories)


@product_router.get("/category/{id}")
async def get_category(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    category = session.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
    return HTTPException(status_code=status.HTTP_200_OK, detail=category)


@product_router.put("/category/{id}")
async def update_category(id: int, category: CategoryModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    exist_category = session.query(Category).filter(Category.id == id).first()
    if not exist_category:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
    exist_category.title = category.title
    exist_category.products_count = category.products_count
    exist_category.photo = category.photo
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="category is successful updated")


@product_router.delete("/categories/{id}")
async def delete_category(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    exist_category = session.query(Category).filter(Category.id ==id).first()
    if not exist_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the category does not exist")
    session.delete(exist_category)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="succesful deleted")


@product_router.get("/{id}")
async def get_product(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    product = session.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The product does not exist")
    return product


@product_router.delete("/{id}")
async def delete_product(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    product = session.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The product does not exist")
    session.delete(product)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="successful deleted")

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from db.database import Base


class Users(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=func.now())

    employee = relationship('OurTeam', back_populates='users')
    comments = relationship('Comments', back_populates='users')
    cart = relationship('Cart', back_populates='user')

    def __repr__(self):
        return self.email


class Status(Base):
    __tablename__ = 'db_models_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    employee = relationship('OurTeam', back_populates='status')

    def __repr__(self):
        return self.name


class OurTeam(Base):
    __tablename__ = 'db_models_ourteam'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('auth_user.id'))
    photo = Column(String(255))
    status_id = Column(Integer, ForeignKey('db_models_status.id'))
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    status = relationship('Status', back_populates='employee')
    users = relationship('Users', back_populates='employee')

    def __repr__(self):
        return self.name


class Comments(Base):
    __tablename__ = 'db_models_comments'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('auth_user.id'))
    text = Column(Text)
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    users = relationship('Users', back_populates='comments')
    product = relationship('Product', back_populates='comments')

    def __repr__(self):
        return self.text


class Category(Base):
    __tablename__ = 'db_models_category'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    products_count = Column(Integer, default=0)
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    product = relationship('Product', back_populates='category')

    def __repr__(self):
        return self.title


class Product(Base):
    __tablename__ = 'db_models_product'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    manufacturer_name = Column(String(100))
    discount = Column(Float, default=0)
    image = Column(String(255))
    popular_products = Column(Integer, default=0)
    price = Column(Float)
    price_type = Column(String(10), default='$')
    rating = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey('db_models_category.id'))
    comments_id = Column(Integer, ForeignKey('db_models_comments.id'))
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    comments = relationship('Comments', back_populates='product')
    category = relationship('Category', back_populates='product')
    cart = relationship('Cart', back_populates='product')

    def __repr__(self):
        return self.name


class Cart(Base):
    __tablename__ = 'db_models_cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('db_models_product.id'))
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    product_number = Column(Integer, default=1)
    payment_status = Column(Boolean, default=False)
    total_price = Column(Float, default=0)
    price_type = Column(String(10))
    created_date = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    product = relationship('Product', back_populates='cart')
    user = relationship('Users', back_populates='cart')

    def __repr__(self):
        return self.total_price

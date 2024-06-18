from db.database import ENGINE, Base
from db.models import Users, Status, OurTeam, Comments, Category, Product, Cart


Base.metadata.create_all(bind=ENGINE)

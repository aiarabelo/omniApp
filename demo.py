import virtualenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import func

engine = create_engine("sqlite:///:memory:")  # connecting

Session = sessionmaker(bind=engine)  # attach primary key to object

session = Session()

Base = declarative_base()


class Cookie(Base):  # must inherit from the base object

    __tablename__ = (
        "cookies"
    )  # Tells us where in the database we're going to store it, must define a table name

    cookie_id = Column(
        Integer, primary_key=True
    )  # Must have one or more columns with primary_key
    cookie_name = Column(
        String(50), index=True
    )  # Don't put nothing in the string paranthesis; dangerous and risky otherwise
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))


Base.metadata.create_all(engine)

# Adding a cookie
cc_cookie = Cookie(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://www.google.com",
    cookie_sku="CC01",
    quantity=12,
    unit_cost=0.5,
)

# Adding to session

session.add(cc_cookie)  # nothing happens until it's committed
session.commit()  # Don't have to commit every transaction, you can just flush


# Bulk Inserts

c1 = Cookie(
    cookie_name="peanut butter",
    cookie_recipe_url="http://www.google.com",
    cookie_sku="PB01",
    quantity=24,
    unit_cost=0.25,
)

c2 = Cookie(
    cookie_name="oatmeal raisin",
    cookie_recipe_url="http://www.google.com",
    cookie_sku="EWW01",
    quantity=100,
    unit_cost=1.00,
)

session.bulk_save_objects([c1, c2])  # Bulk
session.commit()

for cookie in session.query(Cookie):
    print(cookie)


for cookie in session.query(Cookie).order_by(Cookie.quantity):
    print("{:3} - {}".format(cookie.quantity, cookie.cookie_name))

for cookie in session.query(Cookie).order_by(Cookie.quantity).limit(2):
    print("{:3} - {}".format(cookie.quantity, cookie.cookie_name))

query = session.query(Cookie).order_by(Cookie.quantity).limit(2)
print([result.cookie_name for result in query])

print(session.query(Cookie.cookie_name, Cookie.quantity).first())

print(c1.cookie_name)  # accessing attributes

inv_count = session.query(func.sum(Cookie.quantity)).scalar()
print(inv_count)
# if you don't call scalar:
rec_count = session.query(func.count(Cookie.cookie_name)).first()
print(rec_count)  # (3,0)
# Labeling:
rec_count = session.query(
    func.count(Cookie.cookie_name).label("inventory_count")
).first()
print(rec_count.keys())  # ['inventory_count']
print(rec_count.inventory_count)  # 3

record = session.query(Cookie).filter_by(cookie_name="chocolate chip").first()
print("Filter by allows us to define a column")
print(record)

# Filter instead, tells us specifically
record = session.query(Cookie).filter(Cookie.cookie_name == "Chocolate chip").first()
print(record)

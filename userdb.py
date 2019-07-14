from sqlalchemy import Table, COlumn, Integer, String, MetaData, ForeignKey
metadata = MetaData()
users = Table('users', metadata,
        Column('id', Integer, primary_key = True)
        Column('name', String)
        Column('fullname', String),
)

addresses = Table('addresses', metadata,
        Column('id', Integer, primary_key = True),
        Column('user_id', None, ForeignKey('users.id')),
        Column('email_address', String, nullable = False)

)

print(users)
print(addresses)
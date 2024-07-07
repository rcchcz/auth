from sqlalchemy import Column, String, create_engine, UniqueConstraint, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///local_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Auth(Base):
    __tablename__ = 'auth'
    microservice = Column(String(50), primary_key=True)
    token = Column(String(255), unique=True, nullable=False)
    UniqueConstraint('microservice', name='unique_microservice')


# Create the tables in the database
Base.metadata.create_all(engine)


# Create a sessionmaker factory
# SessionLocal = sessionmaker(bind=engine)

# INSERT A NEW RECORD ON DATABASE
def insert_new_records(new_data):
    session = SessionLocal()

    meta = MetaData()
    meta.reflect(bind=engine)

    for data in new_data:
        try:
            # Add new entry to the session
            new_entry = Auth(microservice=data["microservice"], token=data["token"])
            session.add(new_entry)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Failed to insert: {data['microservice']} due to unique constraint")

    session.close()


def get_all():
    session = SessionLocal()

    meta = MetaData()
    meta.reflect(bind=engine)
    rec = session.query(Auth).all()

    if rec:
        for r in rec:
            print(r.microservice)


# THIS INSERTION DELETES ALL EXISTING RECORDS BEFORE INSERTING NEW ONES
def first_insert(new_data):
    # Create a new session
    session = SessionLocal()

    meta = MetaData()
    meta.reflect(bind=engine)
    table = meta.tables.get('auth')
    session.execute(table.delete())
    session.commit()

    for data in new_data:
        try:
            # Add new entry to the session
            new_entry = Auth(microservice=data["microservice"], token=data["token"])
            session.add(new_entry)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Failed to insert: {data['microservice']} due to unique constraint")

    session.close()


if __name__ == "__main__":
    get_all()

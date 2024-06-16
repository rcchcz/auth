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

# Function to insert rows into the database
def insert_rows():
    # Create a new session
    session = SessionLocal()

    new_data = [
        {"microservice": "rabbitmq", "token": "$argon2id$v=19$m=65536,t=3,p=4$gmTWdyaVioaDzoXi+Zi7CA$CqPj7mGICVcM4uCcExDH1zacKUMF6ShrirBrt99DH2U"},
        {"microservice": "database", "token": "$argon2id$v=19$m=65536,t=3,p=4$13a6vnlRHiR2jjC6u/Rc6w$LJuTeTRFhplfm87cs8t8k3dt7fRMJpaNllsvFKxNPnE"},
        {'microservice': 'dns', 'token': '$argon2id$v=19$m=65536,t=3,p=4$EgOOQAdv7q8Rok6muE0Jrw$1P92xuM/XYjdlbN58Fv1lQLLa8FTsvJboMnuitWZHX8'}
    ]
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

    ms = session.query(Auth).all()
    print('------------------------------------------------------------------------------------------------------------')
    for m in ms:
        print(f'{m.microservice:<10} | {m.token}')
    print('------------------------------------------------------------------------------------------------------------')

    session.close()

# Main execution
if __name__ == "__main__":
    insert_rows()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastDB'
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/fastDB"
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://ebfuncity_ebfuncity:FastDB2024@74.50.122.78:3306/ebfuncity_fastDB'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=10, pool_timeout=5)
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

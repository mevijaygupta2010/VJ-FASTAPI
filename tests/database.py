
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db,Base
import pytest
from app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL='postgresql://postgres:password123@localhost:5432/postgres_test'

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)



# Base = declarative_base()

# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] =override_get_db

# client= TestClient(app)
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    #run our code before  we run our test
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    #if you use alembic then you can use command.upgrade("head")
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] =override_get_db
    yield TestClient(app)
    
    #run our code after our test finished
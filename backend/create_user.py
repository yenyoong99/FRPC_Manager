from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Admin  
from auth import get_password_hash 
from database import engine  

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def create_user():
    username = "admin"
    password = "admin123456"

    hashed_password = get_password_hash(password)

    user = Admin(username=username, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    print("User created successfully!")


if __name__ == "__main__":
    create_user()
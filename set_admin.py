# set_admin.py  -- run from the backend folder (venv activated)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_settings, Base
from app.models import Admin
from app.auth import hash_password

settings = get_settings()
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def set_admin(username: str, password: str):
    Base.metadata.create_all(bind=engine)
    db = Session()
    try:
        db.query(Admin).delete()  # clear old admin(s)
        db.add(Admin(username=username, password_hash=hash_password(password)))
        db.commit()
        print(f"✅ Admin user set: {username}")
    finally:
        db.close()

if __name__ == "__main__":
    set_admin("admin", "admin123")   # change if you want

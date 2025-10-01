import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, settings, get_db
from .models import Admin
from .auth import hash_password
from .routes import auth as auth_routes
from .routes import gallery as gallery_routes


app = FastAPI(title="Portrait Photography API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables and ensure default admin at startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # seed admin if empty
    from sqlalchemy.orm import Session
    db = Session(bind=engine)
    try:
        count = db.query(Admin).count()
        if count == 0:
            admin = Admin(username="admin", password_hash=hash_password("admin123"))
            db.add(admin)
            db.commit()
    finally:
        db.close()

# Mount uploads static
uploads_path = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

# Routes
app.include_router(auth_routes.router)
app.include_router(gallery_routes.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}

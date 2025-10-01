from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models
from ..auth import verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=schemas.TokenOut)
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == payload.username).first()
    if not admin or (not verify_password(payload.password, admin.password_hash)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token(subject=admin.username)
    return {"access_token": token, "token_type": "bearer"}

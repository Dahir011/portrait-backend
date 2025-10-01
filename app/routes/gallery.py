import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models
from ..auth import get_current_admin

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
UPLOAD_DIR = os.path.abspath(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

@router.get("", response_model=schemas.GalleryListOut)
def list_gallery(db: Session = Depends(get_db)):
    items = db.query(models.Gallery).order_by(models.Gallery.id.desc()).all()
    return {"items": items}

@router.post("", response_model=schemas.GalleryOut)
def create_gallery_item(
    title: str = Form(""),
    category: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _admin = Depends(get_current_admin),
):
    # Ensure image extension
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Only .jpg/.jpeg/.png/.webp allowed")
    fname = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(UPLOAD_DIR, fname)

    with open(dest, "wb") as f:
        f.write(file.file.read())

    image_url = f"/uploads/{fname}"
    g = models.Gallery(title=title, category=category, image_url=image_url)
    db.add(g)
    db.commit()
    db.refresh(g)
    return g

@router.put("/{item_id}", response_model=schemas.GalleryOut)
def update_gallery_item(
    item_id: int,
    title: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _admin = Depends(get_current_admin),
):
    item = db.query(models.Gallery).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if title is not None:
        item.title = title
    if category is not None:
        item.category = category

    if file is not None:
        _, ext = os.path.splitext(file.filename)
        ext = ext.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(status_code=400, detail="Only .jpg/.jpeg/.png/.webp allowed")
        fname = f"{uuid.uuid4().hex}{ext}"
        dest = os.path.join(UPLOAD_DIR, fname)
        with open(dest, "wb") as f:
            f.write(file.file.read())
        # delete old if local file
        try:
            old_path = os.path.join(UPLOAD_DIR, os.path.basename(item.image_url))
            if os.path.exists(old_path):
                os.remove(old_path)
        except Exception:
            pass
        item.image_url = f"/uploads/{fname}"

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_admin),
):
    item = db.query(models.Gallery).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # remove file
    try:
        old_path = os.path.join(UPLOAD_DIR, os.path.basename(item.image_url))
        if os.path.exists(old_path):
            os.remove(old_path)
    except Exception:
        pass

    db.delete(item)
    db.commit()
    return {"ok": True}

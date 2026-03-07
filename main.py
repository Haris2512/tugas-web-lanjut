from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

# Otomatis membuat tabel di SQLite saat aplikasi berjalan
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tugas 3 API Haris")

# Fungsi untuk mengelola koneksi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- JAWABAN TUGAS START ---

# 1. Endpoint GET /items/
@app.get("/items/", response_model=list[schemas.ItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

# 2. Endpoint GET /items/{id}
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return item

# --- JAWABAN TUGAS END ---

# (BONUS) Endpoint POST: Wajib ada supaya kamu bisa isi data dummy untuk di-test
@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
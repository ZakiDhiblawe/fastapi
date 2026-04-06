from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Item
from database import session, engine
from run_models import Base
import run_models
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

obj = FastAPI()
obj.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

items = [
    Item(id=1, name="Item 1", description="Description of Item 1", price=10.0),
    Item(id=2, name="Item 2", description="Description of Item 2", price=20.0),
    Item(id=3, name="Item 3", description="Description of Item 3", price=30.0),
    Item(id=4, name="Item 4", description="Description of Item 4", price=40.0),
]

def init_db():
    db = session()
    count = db.query(run_models.Item).count()
    if count > 0:
        db.close()
        return
    for item in items:
        db.add(run_models.Item(**item.model_dump()))
    db.commit()
    db.close()

init_db()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@obj.get("/")
def greet():
    return "Hello, World!"

@obj.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(run_models.Item).all()

@obj.get("/item/{item_id}")
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    return db.query(run_models.Item).filter(run_models.Item.id == item_id).first()

@obj.post("/item")
def create_item(item: Item, db: Session = Depends(get_db)):
    db.add(run_models.Item(**item.model_dump()))
    db.commit()
    db.refresh(run_models.Item)
    return item

@obj.put("/item")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(run_models.Item).filter(run_models.Item.id == item_id).first()
    if not db_item:
        return {"message": "Item not found"}
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@obj.delete("/item")
def delete_item(item_id:int, db: Session = Depends(get_db)):
    db_item = db.query(run_models.Item).filter(run_models.Item.id == item_id).first()
    if not db_item:
        return {"message": "Item not found"}
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
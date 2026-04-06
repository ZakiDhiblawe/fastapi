from fastapi import FastAPI
from models import Item
obj = FastAPI()

items = [
    Item(id=1, name="Item 1", description="Description of Item 1", price=10.0),
    Item(id=2, name="Item 2", description="Description of Item 2", price=20.0),
    Item(id=3, name="Item 3", description="Description of Item 3", price=30.0),
    Item(id=4, name="Item 4", description="Description of Item 4", price=40.0),
]
@obj.get("/")
def greet():
    return "Hello, World!"

@obj.get("/items")
def get_items():
    return items

@obj.get("/item/{item_id}")
def get_item_by_id(item_id: int):
    
    for item in items:
        if item.id == item_id:
            return item
    return "Item not found"

@obj.post("/item")
def create_item(item: Item):
    items.append(item)
    return item

@obj.put("/item")
def update_item(item_id: int, item:Item):
    for i in range(len(items)):
        if items[i].id == item_id:
            items[i] = item
            return {
                "message": "Item updated successfully",
                "item": item
            }
            
    return "no item found"

@obj.delete("/item")
def delete_item(item_id:int):
    for i in range(len(items)):
        if items[i].id == item_id:
            del items[i]
            return "deleted"
    return "not deleted"
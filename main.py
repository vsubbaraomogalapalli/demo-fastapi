from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Demo API", version="1.0.0")

# In-memory store
items: dict[int, dict] = {}
next_id = 1


class Item(BaseModel):
    name: str
    description: str
    price: float


class ItemResponse(Item):
    id: int


# --- API 1: Items CRUD ---

@app.get("/items", response_model=List[ItemResponse], tags=["Items"])
def list_items():
    """Return all items."""
    return [{"id": k, **v} for k, v in items.items()]


@app.post("/items", response_model=ItemResponse, status_code=201, tags=["Items"])
def create_item(item: Item):
    """Create a new item."""
    global next_id
    items[next_id] = item.model_dump()
    response = {"id": next_id, **items[next_id]}
    next_id += 1
    return response


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int):
    """Get a single item by ID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id]}


@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]


# --- API 2: Health Check ---

@app.get("/health", tags=["Health"])
def health_check():
    """Return service health status."""
    return {
        "status": "healthy",
        "total_items": len(items),
        "version": app.version,
    }

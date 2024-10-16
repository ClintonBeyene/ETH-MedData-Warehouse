from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
from fastapi.responses import HTMLResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}

# Below are 3 endpoints to get items
@app.get('/products/', response_model=list[schemas.Product])
def read_products(limit: int=10, db: Session = Depends(get_db)):
    products = crud.get_items(models.Products, db, limit=limit)
    return products

@app.get('/telegram/', response_model= list[schemas.Telegram])
def read_telegram_datas(limit: int=10, db: Session = Depends(get_db)):
    telegram = crud.get_items(models.Telegram, db, limit=limit)
    return telegram

@app.get('/detected-images/', response_model= list[schemas.Detected_Images])
def read_detected_images(limit: int =10, db: Session = Depends(get_db)):
    detected_images = crud.get_items(models.Detected_Images, db, limit=limit)
    return detected_images


# Below are 3 endpoints to get items by id
@app.get('/products/{item_id}', response_model=schemas.Product)
def read_product(item_id: int, db: Session = Depends(get_db)):
    product = crud.get_item_by_id(models.Products, db, item_id=item_id)
    return product

@app.get('/telegram/{item_id}', response_model=schemas.Telegram)
def read_telegram_data(item_id: int, db: Session = Depends(get_db)):
    telegram = crud.get_item_by_id(models.Telegram, db, item_id=item_id)
    return telegram

@app.get('/detected-images/{item_id}', response_model= schemas.Detected_Images)
def read_detected_image(item_id: int, db: Session = Depends(get_db)):
    image = crud.get_item_by_id(models.Detected_Images, db, item_id=item_id)
    return image


# Below are endpoints to create items
@app.post('/products/', response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_item(models.Products, db=db, item=product)

@app.post('/telegram/', response_model=schemas.Telegram)
def create_telegram(telegram: schemas.TelegramCreate, db: Session = Depends(get_db)):
    return crud.create_item(models.Telegram, db=db, item=telegram)

@app.post('/detected-images/', response_model= schemas.Detected_Images)
def create_image(image: schemas.Detected_Image_Create, db: Session = Depends(get_db)):
    return crud.create_item(models.Detected_Images, db=db, item=image)


# Below are endpoint to delete items
@app.delete('/products/{item_id}', response_model=schemas.Product)
def delete_product(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(models.Products, db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Product ID not found")
    return item

@app.delete('/telegram/{item_id}', response_model=schemas.Telegram)
def delete_telegram(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(models.Telegram, db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Telegram ID not found")
    return item

@app.delete('/detected-images/{item_id}', response_model=schemas.Detected_Images)
def delete_image(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(models.Detected_Images, db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Detected image ID not found")
    return item

# Below are endpoints to update items
@app.put('/products/{item_id}', response_model=schemas.Product)
def update_product(item_id: int, product_update: schemas.Product, db: Session = Depends(get_db)):
    update_data = product_update.dict(exclude_unset=True)
    product = crud.update_item(models.Products, db, item_id=item_id, update_data=update_data)
    if product is None:
        raise HTTPException(status_code=404, detail="Product ID not found")
    return product

@app.put('/telegram/{item_id}', response_model=schemas.Telegram)
def update_telegram(item_id: int, telegram_update: schemas.Telegram, db: Session = Depends(get_db)):
    update_data = telegram_update.dict(exclude_unset=True)
    telegram = crud.update_item(models.Telegram, db, item_id=item_id, update_data=update_data)
    if telegram is None:
        raise HTTPException(status_code=404, detail="Telegram ID not found")
    return telegram

@app.put('/detected-images/{item_id}', response_model=schemas.Detected_Images)
def update_detected_image(item_id: int, image_update: schemas.Detected_Images, db: Session = Depends(get_db)):
    update_data = image_update.dict(exclude_unset=True)
    image = crud.update_item(models.Detected_Images, db, item_id=item_id, update_data=update_data)
    if image is None:
        raise HTTPException(status_code=404, detail="Detected image ID not found")
    return image
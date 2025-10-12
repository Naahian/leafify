from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from app.schemas.product_schema import (
    ProductResponse,

    ProductUpdate,
    CompletePlantProductCreate,
    CompleteAccessoryProductCreate,
)
from app.crud.product_crud import (
    create_product,
    get_all_products,
    get_product,
    get_products_by_type,
    get_products_in_stock,
    update_product,
    delete_product
)
from app.crud.plant_crud import create_plant, delete_plant
from app.crud.accesory_crud import create_accessory, delete_accessory




router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/plant", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_complete_plant_product(
    plant_product: CompletePlantProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = get_product(db, product_id=plant_product.product.id)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID already exists"
        )
    
    # Ensure product type is 'plant'
    if plant_product.product.type != "plant":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product type must be 'plant'"
        )
    
    # Ensure plant ID matches product ID
    if plant_product.plant.id != plant_product.product.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plant ID must match Product ID"
        )
    
    try:
        db_product = create_product(db=db, product=plant_product.product)
        create_plant(db=db, plant=plant_product.plant)
        db.refresh(db_product)
        return db_product
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating plant product: {str(e)}"
        )


@router.post("/accessory", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_complete_accessory_product(
    accessory_product: CompleteAccessoryProductCreate,
    db: Session = Depends(get_db)
):
    # Check if product ID already exists
    existing_product = get_product(db, product_id=accessory_product.product.id)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID already exists"
        )
    
    # Ensure product type is 'accessory'
    if accessory_product.product.type != "accessory":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product type must be 'accessory'"
        )
    
    # Ensure accessory ID matches product ID
    if accessory_product.accessory.id != accessory_product.product.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Accessory ID must match Product ID"
        )
    
    try:
        db_product = create_product(db=db, product=accessory_product.product)
        create_accessory(db=db, accessory=accessory_product.accessory)        
        db.refresh(db_product)
        return db_product
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating accessory product: {str(e)}"
        )


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_type: Optional[str] = Query(None, regex="^(plant|accessory)$"),
    in_stock: bool = Query(False),
    db: Session = Depends(get_db)
):

    if in_stock:
        products = get_products_in_stock(db)
    elif product_type:
        products = get_products_by_type(db, product_type=product_type)
    else:
        products = get_all_products(db, skip=skip, limit=limit)
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id=product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_by_id(
    product_id: str,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    # Check if product exists
    existing_product = get_product(db, product_id=product_id)
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    updated_product = update_product(db=db, product_id=product_id, product=product_update)
    
    return updated_product



@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    # Check if product exists
    existing_product = get_product(db, product_id=product_id)
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    try:
        # Delete related entities first
        if existing_product.type == "plant" and existing_product.plant:
            delete_plant(db=db, plant_id=product_id)
        elif existing_product.type == "accessory" and existing_product.accessory:
            delete_accessory(db=db, accessory_id=product_id)
        
        delete_product(db=db, product_id=product_id)
        
        return None
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )
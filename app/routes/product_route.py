from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.plant_model import Plant
from app.schemas.plantguide_schema import PlantGuideCreate
from database import get_db
from app.schemas.product_schema import (
    AccessoryCreate,
    PlantCreate,
    ProductResponse,
    ProductUpdate,
    CompletePlantProductCreate,
    CompleteAccessoryProductCreate,
)
from app.crud.product_crud import (
    create_product,
    get_all_products,
    get_product,
    get_product_by_name,
    get_products_by_type,
    get_products_in_stock,
    update_product,
    delete_product,
)
from app.crud.plant_crud import create_plant, delete_plant
from app.crud.accesory_crud import create_accessory, delete_accessory


router = APIRouter(prefix="/products", tags=["Products"])


# CREATE PLANT PRODUCT
@router.post(
    "/plant", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_complete_plant_product(
    plant_product: CompletePlantProductCreate, db: Session = Depends(get_db)
):
    existing_product = get_product_by_name(db, product_name=plant_product.product.name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists",
        )

    # Ensure product type is 'plant'
    if plant_product.product.type != "plant":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product type must be 'plant'",
        )

    try:
        db_product = create_product(db=db, product=plant_product.product)

        # Create plant with the product's ID
        plant_data = plant_product.plant.dict()
        plant_data["id"] = db_product.id

        plant_create = PlantCreate(**plant_data)
        create_plant(db=db, plant=plant_create)

        if plant_product.plant_guide:
            from app.crud.plantguide_crud import create_plant_guide

            # Set the plant_guide ID if needed
            plant_guide_data = plant_product.plant_guide.dict()
            plant_guide_data["plant_id"] = db_product.id

            plant_guide_create = PlantGuideCreate(**plant_guide_data)
            create_plant_guide(db=db, plant_guide=plant_guide_create)

        db.refresh(db_product)
        return db_product.to_dict()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating plant product: {str(e)}",
        )


# CREATE ACCESSORY PRODUCT
@router.post(
    "/accessory", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_complete_accessory_product(
    accessory_product: CompleteAccessoryProductCreate, db: Session = Depends(get_db)
):
    existing_product = get_product_by_name(
        db, product_name=accessory_product.product.name
    )
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists",
        )

    # Ensure product type is 'accessory'
    if accessory_product.product.type != "accessory":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product type must be 'accessory'",
        )

    try:
        db_product = create_product(db=db, product=accessory_product.product)

        # Create accessory with the product's ID
        accessory_data = accessory_product.accessory.dict()
        accessory_data["id"] = db_product.id

        accessory_create = AccessoryCreate(**accessory_data)
        create_accessory(db=db, accessory=accessory_create)

        db.refresh(db_product)
        return db_product.to_dict()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating accessory product: {str(e)}",
        )


# GET ALL PRODUCTS
@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_type: Optional[str] = Query(None, regex="^(plant|accessory)$"),
    in_stock: bool = Query(False),
    db: Session = Depends(get_db),
):
    if in_stock:
        products = get_products_in_stock(db)
    elif product_type:
        products = get_products_by_type(db, product_type=product_type)
    else:
        products = get_all_products(db, skip=skip, limit=limit)

    return products


# GET PRODUCT BY ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    product = get_product(db, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


# UPDATE PRODUCT BY ID
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_by_id(
    product_id: str, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    existing_product = get_product(db, product_id=product_id)
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    updated_product = update_product(
        db=db, product_id=product_id, product=product_update
    )

    return updated_product


# DELETE PRODUCT BY ID
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(product_id: str, db: Session = Depends(get_db)):

    existing_product = get_product(db, product_id=product_id)
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
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
            detail=f"Error deleting product: {str(e)}",
        )

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict

from database import get_db
from app.schemas.plantguide_schema import (
    PlantGuideResponse,
    PlantGuideCreate,
    PlantGuideUpdate,
)
from app.crud.plantguide_crud import (
    create_plant_guide,
    get_all_plant_guides,
    get_plant_guide,
    update_plant_guide,
    delete_plant_guide,
)
from app.crud.plant_crud import get_plant

router = APIRouter(prefix="/plant-guides", tags=["Plant Guides"])


# GET ALL PLANT GUIDES
@router.get("/", response_model=List[PlantGuideResponse])
async def get_guides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    guides = get_all_plant_guides(db, skip=skip, limit=limit)
    return guides


# GET PLANT GUIDE BY PLANT ID
@router.get("/{plant_id}", response_model=PlantGuideResponse)
async def get_guide_by_plant_id(plant_id: str, db: Session = Depends(get_db)):
    guide = get_plant_guide(db, plant_id=plant_id)

    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}",
        )

    return guide


# CREATE COMPLETE PLANT GUIDE
@router.post(
    "/", response_model=PlantGuideResponse, status_code=status.HTTP_201_CREATED
)
async def create_complete_plant_guide(
    plant_guide: PlantGuideCreate, db: Session = Depends(get_db)
):
    plant = get_plant(db, plant_id=plant_guide.id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_guide.id}",
        )

    existing_guide = get_plant_guide(db, plant_id=plant_guide.id)
    if existing_guide:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plant guide already exists for plant ID: {plant_guide.id}",
        )

    # Validate JSON structures
    if not isinstance(plant_guide.how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object",
        )

    if not isinstance(plant_guide.care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object",
        )

    new_guide = create_plant_guide(db=db, plant_guide=plant_guide)
    return new_guide


# CREATE OR UPDATE HOW TO PLANT SECTION
@router.post(
    "/{plant_id}/how-to-plant",
    response_model=PlantGuideResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_how_to_plant_guide(
    plant_id: str, how_to_plant: Dict, db: Session = Depends(get_db)
):
    plant = get_plant(db, plant_id=plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_id}",
        )

    # Validate JSON structure
    if not isinstance(how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object",
        )

    existing_guide = get_plant_guide(db, plant_id=plant_id)

    if existing_guide:
        guide_update = PlantGuideUpdate(how_to_plant=how_to_plant)
        updated_guide = update_plant_guide(
            db=db, plant_id=plant_id, plant_guide=guide_update
        )
        return updated_guide
    else:
        new_guide_data = PlantGuideCreate(
            id=plant_id, how_to_plant=how_to_plant, care_guide={}
        )
        new_guide = create_plant_guide(db=db, plant_guide=new_guide_data)
        return new_guide


# CREATE OR UPDATE CARE GUIDE SECTION
@router.post(
    "/{plant_id}/care-guide",
    response_model=PlantGuideResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_care_guide(
    plant_id: str, care_guide: Dict, db: Session = Depends(get_db)
):
    plant = get_plant(db, plant_id=plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_id}",
        )

    # Validate JSON structure
    if not isinstance(care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object",
        )

    existing_guide = get_plant_guide(db, plant_id=plant_id)

    if existing_guide:
        guide_update = PlantGuideUpdate(care_guide=care_guide)
        updated_guide = update_plant_guide(
            db=db, plant_id=plant_id, plant_guide=guide_update
        )
        return updated_guide
    else:
        new_guide_data = PlantGuideCreate(
            id=plant_id, how_to_plant={}, care_guide=care_guide
        )
        new_guide = create_plant_guide(db=db, plant_guide=new_guide_data)
        return new_guide


# UPDATE HOW TO PLANT SECTION
@router.patch("/{plant_id}/how-to-plant", response_model=PlantGuideResponse)
async def update_how_to_plant_guide(
    plant_id: str, how_to_plant: Dict, db: Session = Depends(get_db)
):
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}. Use POST to create a new guide.",
        )

    # Validate JSON structure
    if not isinstance(how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object",
        )

    guide_update = PlantGuideUpdate(how_to_plant=how_to_plant)
    updated_guide = update_plant_guide(
        db=db, plant_id=plant_id, plant_guide=guide_update
    )
    return updated_guide


# UPDATE CARE GUIDE SECTION
@router.patch("/{plant_id}/care-guide", response_model=PlantGuideResponse)
async def update_care_guide_section(
    plant_id: str, care_guide: Dict, db: Session = Depends(get_db)
):
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not fqound for plant ID: {plant_id}. Use POST to create a new guide.",
        )

    # Validate JSON structure
    if not isinstance(care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object",
        )

    guide_update = PlantGuideUpdate(care_guide=care_guide)
    updated_guide = update_plant_guide(
        db=db, plant_id=plant_id, plant_guide=guide_update
    )
    return updated_guide


# DELETE PLANT GUIDE BY PLANT ID
@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guides(plant_id: str, db: Session = Depends(get_db)):
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}",
        )

    delete_plant_guide(db=db, plant_id=plant_id)
    return None

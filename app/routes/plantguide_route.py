from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict

from database import get_db
from app.schemas.plantguide_schema import (
    PlantGuideResponse,
    PlantGuideCreate,
    PlantGuideUpdate
)
from app.crud.plantguide_crud import (
    create_plant_guide,
    get_all_plant_guides,
    get_plant_guide,
    update_plant_guide,
    delete_plant_guide
)
from app.crud.plant_crud import get_plant

router = APIRouter(prefix="/plant-guides", tags=["Plant Guides"])


@router.get("/", response_model=List[PlantGuideResponse])
async def get_guides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all plant guides
    - **skip**: Number of guides to skip (pagination)
    - **limit**: Maximum number of guides to return
    """
    guides = get_all_plant_guides(db, skip=skip, limit=limit)
    return guides


@router.get("/{plant_id}", response_model=PlantGuideResponse)
async def get_guide_by_plant_id(
    plant_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific plant guide by plant ID
    """
    guide = get_plant_guide(db, plant_id=plant_id)
    
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}"
        )
    
    return guide


@router.post("/", response_model=PlantGuideResponse, status_code=status.HTTP_201_CREATED)
async def create_complete_plant_guide(
    plant_guide: PlantGuideCreate,
    db: Session = Depends(get_db)
):
    """
    Create a complete plant guide (both how_to_plant and care_guide)
    
    Requires:
    - plant_id: Must match an existing plant
    - how_to_plant: JSON object with planting instructions
    - care_guide: JSON object with care instructions
    """
    # Check if plant exists
    plant = get_plant(db, plant_id=plant_guide.id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_guide.id}"
        )
    
    # Check if guide already exists
    existing_guide = get_plant_guide(db, plant_id=plant_guide.id)
    if existing_guide:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plant guide already exists for plant ID: {plant_guide.id}"
        )
    
    # Validate JSON structures
    if not isinstance(plant_guide.how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object"
        )
    
    if not isinstance(plant_guide.care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object"
        )
    
    # Create plant guide
    new_guide = create_plant_guide(db=db, plant_guide=plant_guide)
    return new_guide


@router.post("/{plant_id}/how-to-plant", response_model=PlantGuideResponse, status_code=status.HTTP_201_CREATED)
async def create_how_to_plant_guide(
    plant_id: str,
    how_to_plant: Dict,
    db: Session = Depends(get_db)
):
    """
    Create or update only the 'how_to_plant' section of a plant guide
    
    If guide doesn't exist, creates a new one with empty care_guide
    If guide exists, updates only the how_to_plant section
    """
    # Check if plant exists
    plant = get_plant(db, plant_id=plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_id}"
        )
    
    # Validate JSON structure
    if not isinstance(how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object"
        )
    
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    
    if existing_guide:
        # Update existing guide
        guide_update = PlantGuideUpdate(how_to_plant=how_to_plant)
        updated_guide = update_plant_guide(db=db, plant_id=plant_id, plant_guide=guide_update)
        return updated_guide
    else:
        # Create new guide with empty care_guide
        new_guide_data = PlantGuideCreate(
            id=plant_id,
            how_to_plant=how_to_plant,
            care_guide={}
        )
        new_guide = create_plant_guide(db=db, plant_guide=new_guide_data)
        return new_guide


@router.post("/{plant_id}/care-guide", response_model=PlantGuideResponse, status_code=status.HTTP_201_CREATED)
async def create_care_guide(
    plant_id: str,
    care_guide: Dict,
    db: Session = Depends(get_db)
):
    """
    Create or update only the 'care_guide' section of a plant guide
    
    If guide doesn't exist, creates a new one with empty how_to_plant
    If guide exists, updates only the care_guide section
    """
    # Check if plant exists
    plant = get_plant(db, plant_id=plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant not found with ID: {plant_id}"
        )
    
    # Validate JSON structure
    if not isinstance(care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object"
        )
    
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    
    if existing_guide:
        # Update existing guide
        guide_update = PlantGuideUpdate(care_guide=care_guide)
        updated_guide = update_plant_guide(db=db, plant_id=plant_id, plant_guide=guide_update)
        return updated_guide
    else:
        # Create new guide with empty how_to_plant
        new_guide_data = PlantGuideCreate(
            id=plant_id,
            how_to_plant={},
            care_guide=care_guide
        )
        new_guide = create_plant_guide(db=db, plant_guide=new_guide_data)
        return new_guide


@router.put("/{plant_id}", response_model=PlantGuideResponse)
async def update_complete_guide(
    plant_id: str,
    plant_guide: PlantGuideUpdate,
    db: Session = Depends(get_db)
):
    """
    Update complete plant guide (can update how_to_plant and/or care_guide)
    """
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}"
        )
    
    # Validate JSON structures if provided
    if plant_guide.how_to_plant is not None and not isinstance(plant_guide.how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object"
        )
    
    if plant_guide.care_guide is not None and not isinstance(plant_guide.care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object"
        )
    
    # Update guide
    updated_guide = update_plant_guide(db=db, plant_id=plant_id, plant_guide=plant_guide)
    return updated_guide


@router.patch("/{plant_id}/how-to-plant", response_model=PlantGuideResponse)
async def update_how_to_plant_guide(
    plant_id: str,
    how_to_plant: Dict,
    db: Session = Depends(get_db)
):
    """
    Update only the 'how_to_plant' section of an existing plant guide
    """
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}. Use POST to create a new guide."
        )
    
    # Validate JSON structure
    if not isinstance(how_to_plant, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="how_to_plant must be a JSON object"
        )
    
    # Update guide
    guide_update = PlantGuideUpdate(how_to_plant=how_to_plant)
    updated_guide = update_plant_guide(db=db, plant_id=plant_id, plant_guide=guide_update)
    return updated_guide


@router.patch("/{plant_id}/care-guide", response_model=PlantGuideResponse)
async def update_care_guide_section(
    plant_id: str,
    care_guide: Dict,
    db: Session = Depends(get_db)
):
    """
    Update only the 'care_guide' section of an existing plant guide
    """
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}. Use POST to create a new guide."
        )
    
    # Validate JSON structure
    if not isinstance(care_guide, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="care_guide must be a JSON object"
        )
    
    # Update guide
    guide_update = PlantGuideUpdate(care_guide=care_guide)
    updated_guide = update_plant_guide(db=db, plant_id=plant_id, plant_guide=guide_update)
    return updated_guide


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guides(
    plant_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a plant guide by plant ID
    """
    # Check if guide exists
    existing_guide = get_plant_guide(db, plant_id=plant_id)
    if not existing_guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant guide not found for plant ID: {plant_id}"
        )
    
    # Delete guide
    delete_plant_guide(db=db, plant_id=plant_id)
    return None
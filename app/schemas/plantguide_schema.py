from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Union



class PlantGuideBase(BaseModel):
    how_to_plant: Dict
    care_guide: Dict


class PlantGuideCreate(PlantGuideBase):
    id: str


class PlantGuideUpdate(BaseModel):
    how_to_plant: Optional[Dict] = None
    care_guide: Optional[Dict] = None


class PlantGuideResponse(PlantGuideBase):
    id: str
    
    class Config:
        from_attributes = True



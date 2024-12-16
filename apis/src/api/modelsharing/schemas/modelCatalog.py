from pydantic import BaseModel
from typing import List
from src.api.modelsharing.schemas.addModel import ModelResponse

class ModelCatalogResponse(BaseModel):
    models: List[ModelResponse]
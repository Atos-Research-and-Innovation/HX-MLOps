from pydantic import BaseModel
from typing import List
from src.api.datasetsharing.schemas.addDataset import DatasetResponse

class DatasetCatalogResponse(BaseModel):
    datasets: List[DatasetResponse]
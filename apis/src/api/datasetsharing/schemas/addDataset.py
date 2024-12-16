from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any


class DataType(str, Enum):
    """Enum for dataType"""
    PRODUCTION = "production"
    SYNTHETIC = "synthetic"
    MIXED = "mixed"

class Dataset(BaseModel):
    name: str
    version: str
    dataType: DataType
    tag: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class DatasetResponse(BaseModel):
    datasetIdentifier: int
    name: str
    version: str
    dataType: DataType
    tag: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
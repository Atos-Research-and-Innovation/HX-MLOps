from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any


class Status(str, Enum):
    """Enum for status"""
    PRODUCTION = "production"
    STAGING = "staging"
    TRAINING = "training"

class Model(BaseModel):
    name: str
    version: str
    status: Status
    library: str
    libraryVersion: str
    domain: str 
    tag: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    characteristics: Dict[str, Any] = Field(default_factory=dict)

class ModelResponse(BaseModel):
    modelIdentifier: int
    name: str
    version: str
    status: Status
    library: str
    libraryVersion: str
    domain: str 
    tag: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    characteristics: Dict[str, Any] = Field(default_factory=dict)
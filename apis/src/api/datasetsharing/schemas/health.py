from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum


class HealthStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"

class HealthResponse(BaseModel):
    status: HealthStatus
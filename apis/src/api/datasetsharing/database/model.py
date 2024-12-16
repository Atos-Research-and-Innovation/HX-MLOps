from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ARRAY,
    Float,
    DateTime,
    ForeignKey,
    Identity,
    JSON
)
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()


class Dataset(Base):

    __tablename__ = "model"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    dataType = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    dataModelPath = Column(String, nullable=False)
    datasetPath = Column(String, nullable=False)
    parameters = Column(JSON)

    def __init__(
        self,
        name,
        version,
        dataType,
        tag,
        dataModelPath,
        datasetPath,
        parameters,):
        self.name = name
        self.version = version
        self.dataType = dataType
        self.tag = tag
        self.dataModelPath = dataModelPath
        self.datasetPath = datasetPath
        self.parameters = parameters
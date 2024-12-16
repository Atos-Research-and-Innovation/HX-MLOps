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


class Model(Base):

    __tablename__ = "model"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    status = Column(String, nullable=False)
    library = Column(String, nullable=False)
    libraryVersion = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    filePath = Column(String, nullable=False)
    parameters = Column(JSON)
    characteristics = Column(JSON)

    def __init__(
        self,
        name,
        version,
        status,
        library,
        libraryVersion,
        domain,
        tag,
        filePath,
        parameters,
        characteristics):
        self.name = name
        self.version = version
        self.status = status
        self.library = library
        self.libraryVersion = libraryVersion
        self.domain = domain
        self.tag = tag
        self.filePath = filePath
        self.parameters = parameters
        self.characteristics = characteristics
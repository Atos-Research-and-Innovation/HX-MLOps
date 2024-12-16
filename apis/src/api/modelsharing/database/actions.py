
from .model import Model
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List


def save_model(model_data, minio_path, db_session: Session):

    new_model = Model(
        name=model_data.name,
        version=model_data.version,
        status=model_data.status,
        library=model_data.library,
        libraryVersion=model_data.libraryVersion,
        domain=model_data.domain,
        tag=model_data.tag,
        filePath=minio_path,
        parameters=model_data.parameters,
        characteristics=model_data.characteristics 
    )

    db_session.add(new_model)
    db_session.commit()
    db_session.refresh(new_model)

    return new_model.id


def get_model_by_id_and_version(model_id: str, version: str, db_session: Session):
    model_data = db_session.query(Model).filter(Model.id == model_id, Model.version == version).first()
    if not model_data:
        raise HTTPException(status_code=404, detail="Model not found")
    return model_data

def delete_model(model_id: str, version: str, db_session: Session):
    model = db_session.query(Model).filter_by(id=model_id, version=version).first()
    if model:
        db_session.delete(model)
        db_session.commit()
    else:
        raise Exception("Model not found")


def get_filtered_models(
    db_session: Session,
    domain: Optional[str] = None,
    tag: Optional[str] = None,
    status: str = "production",
    name: Optional[str] = None,
    version: Optional[str] = None,
):
    query = db_session.query(Model)
    
    if domain:
        query = query.filter(Model.domain == domain)
    if tag:
        query = query.filter(Model.tag == tag)
    if status:
        query = query.filter(Model.status == status)
    if name:
        query = query.filter(Model.name == name)
    if version:
        query = query.filter(Model.version == version)
    
    return query.all()

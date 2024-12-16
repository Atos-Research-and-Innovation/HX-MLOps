
from .model import Dataset
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List


def save_dataset(dataset_data, dataset_path, dataModel_path, db_session: Session):

    new_dataset = Dataset(
        name=dataset_data.name,
        version=dataset_data.version,
        dataType = dataset_data.dataType,
        tag=dataset_data.tag,
        dataModelPath = dataModel_path,
        datasetPath = dataset_path,
        parameters=dataset_data.parameters,
    )

    db_session.add(new_dataset)
    db_session.commit()
    db_session.refresh(new_dataset)

    return new_dataset.id


def get_dataset_by_id_and_version(dataset_id: str, version: str, db_session: Session):
    dataset_data = db_session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.version == version).first()
    if not dataset_data:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset_data

def delete_dataset(dataset_id: str, version: str, db_session: Session):
    dataset = db_session.query(Dataset).filter_by(id=dataset_id, version=version).first()
    if dataset:
        db_session.delete(dataset)
        db_session.commit()
    else:
        raise Exception("Dataset not found")


def get_filtered_datasets(
    db_session: Session,
    tag: Optional[str] = None,
    dataType: Optional[str] = None,
    name: Optional[str] = None,
    version: Optional[str] = None,
):
    query = db_session.query(Dataset)
    
    if tag:
        query = query.filter(Dataset.tag == tag)
    if dataType:
        query = query.filter(Dataset.dataType == dataType)
    if name:
        query = query.filter(Dataset.name == name)
    if version:
        query = query.filter(Dataset.version == version)
    
    return query.all()

#!/bin/sh

uvicorn src.api.datasetsharing.main:app --host 0.0.0.0 --port 8080 --workers 1
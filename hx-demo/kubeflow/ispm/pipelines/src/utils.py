
# Minio paths where files will be stored
MINIO_CODE_PATH = "common/code"
MINIO_DATA_PATH = "common/data"
MINIO_MODEL_OUTPUT_PATH = "artifacts/model"
MINIO_HANDLER_OUTPUT_PATH = "artifacts/handler"
MINIO_MODEL_REPOSITORY_PATH = "repository"

# Container paths where files will be stored
CONTAINER_CODE_PATH = "src_user"
CONTAINER_DATA_PATH = "data"
CONTAINER_MODEL_OUTPUT_PATH = "artifacts/model"
CONTAINER_HANDLER_OUTPUT_PATH = "artifacts/handler"

# Absolute container path where this code will be copied
CONTAINER_APP_PATH = "/app"


# file name for each stage in the pipeline (datagen, trainer, etc...)
DATAGEN_FILENAME = "datagen_pipeline"
TRAINER_FILENAME = "trainer_pipeline"
EVALUATION_FILENAME = "evaluation_pipeline"
HANDLER_FILENAME = "handler_pipeline"
HANDLER_OUTPUT_FILENAME = "handler"


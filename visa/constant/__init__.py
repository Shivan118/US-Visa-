import os
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

CURRENT_TIME_STAMP = get_current_time_stamp()
ROOT_DIR = os.getcwd() # to get current working dir
CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.yaml'

CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)


# data ingested related variable
DATA_INGESTION_CONFIG_KEY  = 'data_ingestion_config'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_INGESTED_DIR_KEY = 'ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'

# traning pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = 'artifact_dir'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'

# Company Variables
COLUMN_COMPANY_AGE = 'company_age'
COLUMN_YEAR_ESTB = 'yr_of_estab'
COLUMN_ID = 'case_id'


## DATA VALIDATION RELATED VARIABLE
DATA_VALIDATION_ARTIFACT_DIR = 'data_validation'
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_yaml'

# data transformation related variable
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_ARTIFACT_DIR = 'data_transformation'
DATA_TRANSFORMATION_KEY_DIR_NAME = 'transformed_dir'
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSING_FILE_NAME_KEY = ' preprocessed_object_file_name'



TARGET_COLUMN_KEY ='target_columns'
DATASET_SCHEMA_COLLUMNS_KEY='ColumnsNames'



NUMERICAL_COLLUMN_KEY  = 'Numerical_columns'
ONE_HOT_COLLUMN_KEY = 'Onehot_columns'
ORDINAL_COLLUMN_KEY = 'Oridanl_columns'
TRANSFORM_COLLUMN_KEY = 'Transformation_columns'


# model_trainer related vriaable

MODEL_TRAINER_ARTIFACT_DIR = 'model_trainer'
MODEL_TRAINER_CONFIG_KEY = 'model_trainer_config'
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = 'trained_model_dir'
MODEL_TRAINER_TRAINED_FILE_NAME_KEY = 'model_file_name'
MODEL_TRAINER_BASE_ACCURACY_KEY = 'base_accuracy'
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = 'model_config_dir'
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = 'model_config_file_name'

# model_evaluation related variable
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_FILE_NAME_KEY = 'model_evaluation_file_name'
MODEL_EVALUATION_ARTIFACT_DIR = 'model_evaluation'

BEST_MODEL_KEY = 'best_model'
HISTORY_KEY = 'history'
MODEL_PATH_KEY = 'model_path'


#model pusher related variable
MODEL_PUSHER_CONFIG_KEY = 'model_pusher_config'
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = 'model_export_dir'
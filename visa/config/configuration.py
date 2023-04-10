import os,sys
from visa.constant import *
from visa.logger import logging
from visa.exception import CustomException
from visa.entity.config_entity import *
from visa.utils.utils import read_yaml_file 


class Configuration:

    def __init__(self,
        config_file_path:str =CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP
        ) -> None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise CustomException(e,sys) from e


    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(
            artifact_dir,
            DATA_INGESTION_ARTIFACT_DIR,
            self.time_stamp
            )

            data_ingestion_info=self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url=data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_train_dir=os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])

            ingested_test_dir=os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config=DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data Ingestion Config: {data_ingestion_config}")
            return data_ingestion_config

        except Exception as e:
            raise CustomException (e,sys) from e
    

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )

            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR,
                                            data_validation_confg[DATA_VALIDATION_SCHEMA_DIR_KEY],
                                            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            data_validation_config = DataValidationConfig(
                    schema_file_path = schema_file_path)

            return data_validation_config

        except Exception as e:
            raise CustomException(e,sys) from e
    

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_transformation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR,
                self.time_stamp 
            )

            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            preprocessed_object_file_path=os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                data_transfromation_config_info[DATA_TRANSFORMATION_PREPROCESSING_FILE_NAME_KEY]
            )
            transformed_train_dir=os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_KEY_DIR_NAME],
                data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY]
            )

            transformed_test_dir = os,path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_KEY_DIR_NAME],
                data_transformation_config_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY]
            )

            data_transformation_config = DataTransformationConfig(
                preprocessed_object_file_path= preprocessed_object_file_path,
                transformed_train_dir= transformed_train_dir,
                transformed_test_dir=transformed_test_dir
            )
            logging.info(f"Data Transformation Config:{data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise CustomException(e,sys) from e

    def get_model_training_config(self)->ModelTrainerConfig :
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            model_trainer_config=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.time_stamp
            )

            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            trainer_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_TRAINED_FILE_NAME_KEY]
            )

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]
            model_trainer_config=ModelTrainerConfig(
                trainer_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path
            )
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            raise CustomException(e,sys) from e



    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = os.path.join(self.training_pipeline_config.artifact_dir,
                                        MODEL_EVALUATION_ARTIFACT_DIR, )

            model_evaluation_file_path = os.path.join(artifact_dir,
                                                    model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])
            response = ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Config: {response}.")
            return response
        except Exception as e:
            raise CustomException(e,sys) from e
    
    def get_model_pusher_config(self)-> ModelPusherConfig:
        try:
            timestamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            get_model_pusher_config_info = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = os.path.join(ROOT_DIR,
                                            model_pusher_config_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY],
                                            time_stamp)

            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f" Model Pusher Config {model_pusher_config}")
            return model_pusher_config
        except Exception as e:
            raise CustomException(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,
                                    training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                    training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f" Training pipeline is completed:{training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise CustomException(e,sys) from e

            

        

                 
                 
                


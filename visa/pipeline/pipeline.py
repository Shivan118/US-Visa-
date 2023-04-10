import sys,os
from datetime import datetime
import uuid
from typing import List
from multiprocessing import Process
import pandas as pd
from threading import Thread
from visa.logger import logging
from visa.constant import *
from visa.exception import CustomException
from visa.entity.config_entity import *
from visa.utils.utils import read_yaml_file
from visa.components.data_ingestion import DataIngestion
from visa.components.data_validation import DataValidation
from visa.components.data_ingestion import DataIngestionArtifact
from visa.components.data_transformation import DataTransformation
from visa.components.model_evaluation import ModelEvaluation
from visa.components.model_pusher import ModelPusher
from visa.components.model_training import ModelTrainer
from visa.components.data_transformation import DataTransformationArtifact
from visa.entity.artifact_entity import DataIngestionArtifact
from visa.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from visa.config.configuration import Configuration

class Pipeline():
    def __init__(self, config:Configuration = Configuration())->None:
        try:
            self.config=config
        except Exception as e:
            raise CustomException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataIngestionArtifact:
        try:
            data_validation=DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=DataIngestionArtifact)
            return data_validation.initiate_data_validation
        except Exception as e:
            raise CustomException(e,sys) from e





    def start_data_transformation(self,
                                  data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_validation_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transfarmation
        except Exception as e:
            raise CustomException(e,sys) from e
    

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                        data_transformation_artifact=data_transformation_artifact,
                                        )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise CustomException(e,sys) from e             

    def start_model_evaluation(self,data_ingestion_artifact:DataIngestionArtifact,
                                data_validation_artifact:DataValidationArtifact,
                                model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_eval=ModelEvaluation(
                model_evaluation_config=self.config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise CustomException(e,sys) from e

    def run_pipeline(self):
        try:
             #data ingestion

            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transfromation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transfromation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact=model_evaluation_artifact)
        except Exception as e:
            raise CustomException(e,sys) from e


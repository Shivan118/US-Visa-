import os ,sys
from visa.constant import *
from visa.logger import logging
from visa.exception import CustomException
from visa.utils.utils import read_yaml_file
from visa.entity.config_entity import DataIngestionConfig,DataValidationConfig
from visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from visa.config.configuration import Configuration
from datetime import datetime
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from visa.entity.raw_data_validation import IngestedDataValidation


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                data_ingestion_artifact:DataIngestionArtifact):

        try:
            logging.info(f"{'>>'*20} Data validation log is started {'>>'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            self.schema_path = self.data_validation_config.schema_file_path
            self.train_data = IngestedDataValidation(
                validation_path=self.data_ingestion_artifact.train_file_path,schema_path=self.schema_path)

            self.test_data = IngestedDataValidation(
                validation_path=self.data_ingestion_artifact.test_file_path,schema_path=self.schema_path)

        except Exception as e:
            raise CustomException(e,sys) from e

    def isFolderPathAvailable(self):
        try:
            # True means available , False means is not available
            isfolder_available=False
            train_path = self.data_ingestion_artifact.train_file_path
            test_path = self.data_ingestion_artifact.test_file_path
            if os.path.exists(train_path):
                if os.path.exists(test_path):
                    isfolder_available=True
            return isfolder_available
        except Exception as e:
            raise CustomException(e,sys) from e


    def is_Validatio_successful(self):
        try:
            validation_ststus=True
            if self.isFolderPathAvailable()==True:
                train_filename=os.path.join(
                    self.data_ingestion_artifact.train_file_path
                )
                is_train_filename_validated = self.train_data.validate_filename(train_filename=train_filename)
                is_train_column_number_validation = self.train_data.validation_column_length()
                is_train_column_name_same = self.train_data.check_columns_name()
                is_train_missing_value_whole_column = self.train_data.missing_value_columns()

                self.train_data.replace_null_values_with_null()

                test_filename=os.path.basename(
                    self.data_ingestion_artifact.test_file_path
                )
                 
                is_test_filename_validated = self.test_data.validate_filename(file_name=test_filename)
                is_test_columns_numbers_validation = self.test_data.validation_column_length()
                is_test_columns_name_same = self.test_data.check_columns_name()
                is_test_missing_value_whole_number = self.test_data.missing_value_columns()
                
                self.test_data.replace_null_values_with_null()
                
                # add log
                if is_train_filename_validated & is_train_column_numbers_validated & is_train_column_name_same & is_train_missing_values_whole_column:
                    pass
                else:
                    validation_status = False
                    logging.info("Check yout Training Data! Validation Failed")
                    raise ValueError(
                        "Check your Training data! Validation failed")

                if  is_test_filename_validated & is_test_columns_numbers_validation & is_test_columns_name_same & is_test_missing_value_whole_number:
                    pass
                else:
                    validation_status = False
                    raise ValueError("Check your training data , validation failed")
                
        except Exception as e:
            raise CustomException(e,sys) from e

    def initiate_data_validation(self):
        try:
            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.schema_path,is_validated=self.is_Validation_successful(),
                message='Data  Validation performed ')
            logging.info(f"Data Validation Artifact :{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20} Data validation log is completed {'>>'*20}")

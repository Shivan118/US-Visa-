import os ,sys
import pandas as pd
import numpy as np
from visa.exception import CustomException
from visa.logger import logging
from visa.entity.config_entity import DataIngestionConfig , DataValidationConfig , DataTransformationConfig
from visa.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact , DataTransformationArtifact
from sklearn.compose import ColumnTransformer
from visa.utils.utils import read_yaml_file , load_data , save_numpy_array_data , save_object ,load_object
from visa.constant import *
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder,OneHotEncoder,PowerTransformer
from imblearn.combine import SMOTEENN






class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                data_ingestion_artifact:DataIngestionArtifact,
                data_validation_artifact:DataValidationArtifact):

        try:
            logging.info(f"{'>>'*20} Data validation log is started {'>>'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifcat=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys) from e
    
    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLLUMN_KEY]
            ordinal_columns = dataset_schema[ORDINAL_COLLUMN_KEY]
            onehot_columns = dataset_schema[ONE_HOT_COLLUMN_KEY]
            transformation_columns = dataset_schema[TRANSFORM_COLLUMN_KEY]
            
            num_pipeline = Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='median')),
            ('scaler',StandardScaler())
            ])

            onehot_pipeline =  Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='median')),
            ('ordinal_encoder' , OridinalEncoder()),
            ('scaler',StandardScaler())
            ])

            ordinal_pipeline =  Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='median')),
            ('one_hot_encoder' , OneHotEncoder()),
            ('scaler',StandardScaler(with_mean=False))
            ])

            transform_pipeline = Pileline(steps=[
            ('scaler',StandardScaler()),
            ('transformed',PowerTransformer())
            ])

            processer = ColumnsTransformer([
            ('num_pipeline',num_pipeline, numerical_columns),
            ('onehot_pipeline',onehot_pipeline,ordinal_columns),
            ('ordinal_pipeline',ordinal_pipeline,onehot_columns),
            ('transform_pipeline',transform_pipeline,transformation_columns)
            ])
            return processer
        except Exception as e:
            raise CustomException(e,sys) from e

    def _remove_outliear_IQR(self,col,df):
        try:
            percentile25 = df[col].quantile(0.25)
            percentile75 = df[col].quantile(0.75)
            iqr=percentile75 - percentile25
            lower_limit = percentile25 - 1.5*iqr
            upper_limit = percentile75 + 1.5*iqr

            df.loc[(df[col]> upper_limit),col]=upper_limit
            df.loc[(df[col]<lower_limit),col]=lower_limit
            return df
        except Exception as e:
            raise CustomException(e,sys) from e

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            processing_obj = self.get_data_transformr_object()

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path=self.data_validation_artifact.schema_file_path

            train_df = load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df = loaed_data(file_path=test_file_path,schema_file_path=schema_file_path)

            schema= read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            numerical_columns = schema[NUMERICAL_COLLUMN_KEY]

            continous_columns = [feature for feature in numerical_columns if len(train_df[feature].unique())>=25]
            

            for col in continous_columns:
                self._remove_outliear_IQR(col=col , df=test_df)

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            # fit transformation
            input_feature_train_arr = processing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = processing_obj.transforme(input_feature_test_df)

            smt = SMOTEENN(random_state=35 , sampling_strategy='minority')
            input_feature_train_arr , target_feature_train_df=smt.fit_resample(input_feature_train_arr,input_feature_train_df)
            input_feature_test_arr, target_feature_test_df=smt.fit_resample(input_feature_test_arr,input_feature_test_df)

            train_arr = np.c_(input_feature_train_arr,np.array(target_feature_train_df))
            test_arr = np.c_(input_feature_test_arr,np.array(target_feature_test_df))

            transformed_train_dir = self.data_transformation-config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_name).replace(".csv",'.npz')
            test_file_path = os.path.basename(test_file_path).replace(".csv",'.npz')

            transformed_train_file_path = os.path.join(transformed_train_dir , train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir , test_file_name)

            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            processing_obj_file_path = self.data_transformation_config.processing_obj_file_path

            save_object(file_path=processing_obj_file_path , obj=processing_obj)

            data_transformation_artifact = DataTransformationArtifat(is_transformed=True,
                                                                    message='Data Transformation is Done',
                                                                    transformed_train_file_path=transformed_train_file_path,
                                                                    transformed_test_file_path=transformed_test_file_path,
                                                                    processing_obj_file_path=processing_obj_file_path)

            return  data_transformation_artifact 
        except Exception as e:
            raise CustomException(e,sys) from e






    
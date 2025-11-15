import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_obeject

@dataclass
class DatatransformationConfig:
    preproceesor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DatatransformationConfig()

    def get_data_transformation_object(self):
        try:
            numerical_columns = ["writing_score","reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler()) 
                ]
            )

            cat_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder(handle_unknown="ignore")),
                ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("num scaling completed")
            
            logging.info("cat columns encoding completed")

            preprocessor=ColumnTransformer(
                [
                ("num_piepline",num_pipeline,numerical_columns),
                ("cat_piepline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiated_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("reading tarin and test is completed")

            logging.info("Obtaing preprocssing Object")

            preprcocessing_obj=self.get_data_transformation_object()

            target_column_names = "math_score"
            numrical_columns = ["writing_score","reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_names],axis=1)
            target_feature_train_df=train_df[target_column_names]

            input_feature_tets_df=test_df.drop(columns=[target_column_names],axis=1)
            target_feature_test_df=test_df[target_column_names]

            logging.info(f"applying preprocessing")

            input_feature_train_arr = preprcocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprcocessing_obj.transform(input_feature_tets_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)

            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("svaed pre OBject")

            save_obeject(

                file_path=self.data_transformation_config.preproceesor_obj_file_path,
                obj=preprcocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preproceesor_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException (e,sys)
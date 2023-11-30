import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from scipy import stats
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer

#Reading CSV file
def episode_read_data():
    df = pd.read_csv("processed_data/cleaned_data_final.csv", index_col=0)
    return df

def episode_x_and_y():
    df = episode_read_data()
    df = df.drop(columns=['name', 'episode', 'deaths'], axis=1)
    df = df[df['isAlive'] == 0].drop(columns="isAlive")

    X = df.drop(columns = ["episode_num", "season"], axis=1)
    y = df[["episode_num"]]
    return X, y

#Preprocessing
def episode_create_pipeline():
    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('cat_transformer', cat_transformer, ['origin'])],
        remainder='passthrough'
    )
    return make_pipeline(preprocessor, LinearRegression())

#Splitting Data
def episode_split_train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)
    # transformer = death_create_pipeline()
    # X_train_processed = pd.DataFrame(transformer.fit_transform(X_train),columns=transformer.get_feature_names_out())
    # X_test_processed = pd.DataFrame(transformer.transform(X_test),columns=transformer.get_feature_names_out())
    return X_train, X_test, y_train, y_test

#Cross Validate Model
def episode_cross_validate_result(model, X_train_processed, y_train):
    cv_results = cross_validate(model, X_train_processed, y_train, cv=5, scoring="neg_mean_absolute_error")
    test = cv_results["test_score"].mean()
    return test

#Predict Y
def episode_prediction(model , X):
    y_pred = model.predict(X)
    return y_pred

#CreateModel
def episode_train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

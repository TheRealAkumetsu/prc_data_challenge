# Imports required packages and functions
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor as HGBR
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def data_manipulation(challenge_df,
                      submission_df):
    """
    Input: pandas dataframe of challenge and submission set
    Output: pandas dataframe with manipulated data for training and prediction
    """

    df1 = challenge_df.copy()
    df2 = submission_df.copy()

    # Import list of icao codes and mtow
    icao_list = pd.read_csv('icao_code-mtow.csv')
    df1 = df1.merge(icao_list, on = 'aircraft_type', how = 'left')
    df2 = df2.merge(icao_list, on = 'aircraft_type', how = 'left')

    columns_to_encode = ['aircraft_type', 'wtc', 'airline', 'country_code_adep', 'country_code_ades']

    for col in columns_to_encode:
        # Combine datasets for current column
        combined_data = pd.concat([df1[col], df2[col]], axis=0)

        # Initialize LabelEncoder
        encoder = LabelEncoder()

        # Fit the encoder on the combined data
        encoder.fit(combined_data)

        # Transform original dataset
        df1[f"{col}_en"] = encoder.transform(df1[col]).astype(np.int32)
        df2[f"{col}_en"] = encoder.transform(df2[col]).astype(np.int32)

    for df in [df1, df2]:
        # Transform dates into datetime objects
        df['date'] = pd.to_datetime(df['date'])
        df['actual_offblock_time'] = pd.to_datetime(df['actual_offblock_time'])
        df['arrival_time'] = pd.to_datetime(df['arrival_time'])
        df['weekday'] = df['date'].dt.weekday

        # Convert datetime to Unix time (seconds since the epoch)
        df['date_unix'] = df['date'].view('int64') // 10 ** 9
        df['arrival_time'] = df['arrival_time'].view('int64') // 10 ** 9


        # Transform date signals into periodical signals
        day = 24 * 60 * 60
        # week = 7 * day
        year = (365.2425) * day

        df['date sin'] = np.sin(df['date_unix'] * (2 * np.pi / day))
        df['year sin'] = np.sin(df['date_unix'] * (2 * np.pi / year))
        df["start_hour"] = df["actual_offblock_time"].dt.hour
        df['arrival day sin'] = np.sin(df['arrival_time'] * (2 * np.pi / day))
    return [df1, df2]


def train_tow_hgbr(challenge_df,
                   feature_cols,
                   model_path='hgbr_model.joblib', test=False):
    """
    Input: Challenge dataframe (flightlist only), path to save the model to
    Output: Trained ML model
    """

    # Define target column
    target_col = 'tow'

    # Assuming 'target_variable' is the name of your target variable column
    X = challenge_df[feature_cols]
    y = challenge_df[target_col]

    # Create and fit the HistGradientBoostingRegressor model
    hgbr = HGBR(random_state=42,
                loss='squared_error',
                min_samples_leaf=16,
                max_depth=9,
                categorical_features=[0, 1, 2, 3, 4, 5, 11, 12],
                max_iter=2000,
                l2_regularization=0.1,
                learning_rate=0.078)

    # If this is a test run (Test = True) implement a train test split
    if test == True:
        #Train test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train model on training data
        hgbr.fit(X_train, y_train)
        # Make predictions
        y_train_pred = hgbr.predict(X_train)
        y_test_pred = hgbr.predict(X_test)
        # Evaluate the model
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        train_r2 = r2_score(y_train, y_train_pred)

        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_r2 = r2_score(y_test, y_test_pred)

        print("Train RMSE:", train_rmse)
        print("Train R^2:", train_r2)
        print("Test RMSE:", test_rmse)
        print("Test R^2:", test_r2)

        # Save the model to a file
        joblib.dump(hgbr, model_path)
    
    else:
        # Train model on wholw challenge set
        hgbr.fit(X, y)

        y_pred = hgbr.predict(X)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        print(f"The RMSE of the trained model is {rmse}")

        # Save the model to a file
        joblib.dump(hgbr, model_path)

    return hgbr


def predict_tow_hgbr(submission_df,
                     feature_cols,
                     model_path="hgbr_model.joblib",
                     submission_path="data/submission.csv"):
    """
    Input: submission dataset, path to the saved model, path to save submission to
    Output: sumbmission with predicted tow
    """

    model = joblib.load(model_path)

    # Assuming 'target_variable' is the name of your target variable column
    X = submission_df[feature_cols]

    # Predict the tow
    y = model.predict(X)

    submission_df['tow'] = y
    result_df = submission_df[["flight_id", "tow"]]

    # Save the predictions
    result_df.to_csv(submission_path, index=False)

    return result_df

import logging
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn import preprocessing
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_hist_gradient_boosting 


logger = logging.getLogger(__name__)

def prepare_dataset(test_size=0.2, random_seed=1):
    dataset = pd.read_csv(
        "./Multi_3_train.csv",
        delimiter=",",
    )
    dataset = dataset.rename(columns=lambda x: x.lower().replace(" ", "_"))
    train_df, test_df = train_test_split(dataset, test_size=test_size, random_state=random_seed)
    return {"train": train_df, "test": test_df}






def train():
    logger.info("Preparing dataset...")
    dataset = prepare_dataset()
    train_df = dataset["train"]
    test_df = dataset["test"]

   
    y_train = train_df["loan_status"]
    X_train = train_df.drop("loan_status", axis=1)
    y_test = test_df["loan_status"]
    X_test = test_df.drop("loan_status", axis=1)

    logger.info("Training model...")
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    model = HistGradientBoostingRegressor(max_iter=50).fit(X_train, y_train)

    y_pred = model.predict(X_test)
    error = mean_squared_error(y_test, y_pred)
    logger.info(f"Test MSE: {error}")

    logger.info("Saving artifacts...")
    Path("artifacts").mkdir(exist_ok=True)
    dump(model, "artifacts/model.joblib")
    dump(scaler, "artifacts/scaler.joblib")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()

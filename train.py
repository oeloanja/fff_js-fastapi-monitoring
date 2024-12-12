import logging
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
#from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


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
    model = RandomForestClassifier(n_estimators= 100, max_depth=5, random_state = 0).fit(X_train, y_train)

    y_pred = model.predict(X_test)

    error = recall_score(y_test, y_pred, average='macro')
    logger.info(f"Test recall_score: {error}")

    logger.info("Saving artifacts...")
    Path("artifacts").mkdir(exist_ok=True)
    dump(model, "artifacts/model.joblib")
    dump(scaler, "artifacts/scaler.joblib")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()

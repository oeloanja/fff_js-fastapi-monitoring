import mlflow
import logging
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split, GridSearchCV
#from mlflow.models import infer_signature
import mlflow.sklearn
import sys
sys.setrecursionlimit(10**7)


mlflow.set_tracking_uri("http://127.0.0.1:7000")
mlflow.sklearn.autolog()

logger = logging.getLogger(__name__)

def prepare_dataset(test_size=0.2, random_seed=1):
    dataset = pd.read_csv(
        "./data_fin.csv",
        delimiter=",",
        dtype={"target": "int"}
    )

    dataset = dataset.rename(columns=lambda x: x.lower().replace(" ", "_"))
    dataset = dataset.dropna() 
    train_df, test_df = train_test_split(dataset, test_size=test_size, random_state=random_seed)
    return {"train": train_df, "test": test_df}

def train_with_gridsearch():
    logger.info("Preparing dataset...")
    dataset = prepare_dataset()
    train_df = dataset["train"]
    test_df = dataset["test"]

    y_train = train_df["target"]
    X_train = train_df.drop("target", axis=1)
    y_test = test_df["target"]
    X_test = test_df.drop("target", axis=1)

    # GridSearch 하이퍼파라미터 설정
    param_grid = {
        "n_estimators": [10, 20, 30, 40, 50, 100 ],
        "max_depth": [3, 5, 7],
        "min_samples_split": [2, 3, 4]
    }

    logger.info("Starting GridSearchCV...")
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring="recall_macro", verbose=2)

    # MLflow Experiment 설정
    mlflow.set_experiment("gridsearch_randomforest_experiment")

    # MLflow 로깅 시작
    with mlflow.start_run():
        # GridSearchCV 학습 수행
        logger.info(f"Training with GridSearchCV...")
        grid_search.fit(X_train, y_train)

        # 최적의 모델 및 하이퍼파라미터 추출
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        logger.info(f"Best Parameters: {best_params}")

        # 최적 모델 평가
        y_pred = best_model.predict(X_test)
        recall = recall_score(y_test, y_pred, average="macro")
        logger.info(f"Test Recall Score: {recall}")

        # MLflow 로깅
        mlflow.log_param("grid_search", True)
        for param, value in best_params.items():
            mlflow.log_param(param, str(value))
        mlflow.log_metric("recall_score", float(recall))
        mlflow.sklearn.log_model(best_model, "best_random_forest_model")

        # 모델 저장 (최적화된 모델)
        logger.info("Saving artifacts...")
        Path("artifacts").mkdir(exist_ok=True)
        dump(best_model, "artifacts/best_model.joblib")
        logger.info("Best model saved to artifacts.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_with_gridsearch()

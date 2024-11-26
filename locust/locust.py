from locust import HttpUser, task
import pandas as pd
import random

feature_columns = {
    
 'loan amnt' : 'loan_amnt',         
  'int rate': 'int_rate',                    
 'installment':'installment',                 
 'grade':'grade',                       
 'emp length':'emp_length',                  
 'annual inc':'annual_inc',                                  
 'dti':'dti',                         
 'open acc':'open_acc',                    
 'pub rec':'pub_rec',                     
 'revol bal':'revol_bal',                   
 'revol util':'revol_util',                  
 'total acc':'total_acc' ,                  
 'collections 12 mths ex med':'collections_12_mths_ex_med', 
 'mort acc':'mort_acc',                    
 'emp':'emp',                         
 'home ownership':'home_ownership',
 'purpose':'purpose',
 'earliest cr line':'earliest_cr_line',
 'issue d':'issue_d',

}

dataset = (
    pd.read_csv(
        "./Multi_3_train.csv",
        delimiter=",",
    )
    .rename(columns=feature_columns)
    .drop("loan_status", axis=1)
    .to_dict(orient="records")
)

class LoanPredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        record = random.choice(dataset).copy()
        self.client.post("/predict", json=record)

    @task(2)
    def prediction_bad_value(self):
        record = random.choice(dataset).copy()
        corrupt_key = random.choice(list(record.keys()))
        record[corrupt_key] = "bad data"
        self.client.post("/predict", json=record)
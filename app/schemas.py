from pydantic import BaseModel, Field

feature_names = [

    "int_rate",
    "installment",
    "dti",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "open_acc",
    "total_acc",
    "mort_acc",
    "collections_12_mths_ex_med",
    "annual_inc",
    "loan_amnt",
    "cr_line_period",
    "issue_d_period",
    "emplength",
    "loan_purpose",
    
]


class Loan(BaseModel):
    
    int_rate : float = Field(
        ...,  description = "The interest rate on the loan."
    )
    installment : float = Field(
        ...,  description = "The monthly payment amount for the loan."
    )
    dti : float = Field(
        ..., description = "Debt-to-income ratio, calculated as the borrower’s monthly debt payments divided by their monthly income."
    )
    pub_rec : float = Field(
        ..., description = "The number of derogatory public records in the borrower’s credit history."
    )
    revol_bal : float = Field(
        ..., description = "The total credit revolving balance."
    )
    revol_util : float = Field(
        ..., description = "The revolving line utilization rate, or the amount of credit used relative to the total available credit."
    )
    open_acc : float = Field(
        ..., description = "The number of open credit lines in the borrower’s credit history."
    ) 
    total_acc : float = Field(
        ...,  description = "The total number of credit accounts the borrower has."
    )
    mort_acc : float = Field(
        ..., description = "The number of mortgage accounts."
    )   
    collections_12_mths_ex_med : float = Field(
        ..., description = "The number of collections in the past 12 months, excluding medical collections."
    )
    annual_inc : float = Field(
        ...,  description = "The borrower’s annual income."
    )    
    loan_amnt : float = Field(
        ..., description = "The amount of money requested for the loan."
    )
    cr_line_period : int = Field (
        ..., description = "Represents the number of days the borrower has had a credit line."
    )
    issue_d_period : int = Field(
        ..., description = " Indicates the date when the loan was issued."
    ) 
    emplength : int = Field(
        ...,  description = "The length of the borrower’s employment in years."
    )
    loan_purpose : int = Field(
        ..., description= "loan purpose."
    )


class Rating(BaseModel):
    target: int = Field(
        ...,
        ge = 0,
        le = 2,
        description = "The current status of the loan (e.g., fully paid, charged off)."
    )




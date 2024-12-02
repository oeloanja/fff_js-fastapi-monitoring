from pydantic import BaseModel, Field

feature_names = [
    
 "loan_amnt",                   
 "int_rate",                    
 "installment",                 
 "grade",                       
 "emp_length",                 
 "annual_inc",                                  
 "dti",                         
 "open_acc",                    
 "pub_rec",                     
 "revol_bal",                   
 "revol_util",                  
 "total_acc",                   
 "collections_12_mths_ex_med", 
 "mort_acc",                    
 "emp",                         
 "home_ownership",
 "purpose",
 "earliest_cr_line",
 "issue_d"
]


## ge : greater than or equal / le : less than or equal

class loan(BaseModel):
    loan_amnt : float = Field(
        ..., ge=0 , description = "The amount of money requested for the loan."
    )
    int_rate : float = Field(
        ..., ge=0 , description = "The interest rate on the loan."
    )
    installment : float = Field(
        ..., ge=0 , description = "The monthly payment amount for the loan."
    )
    grade : float = Field(
        ..., ge=0 , description = "The credit grade assigned to the loan."
      
    )
    emp_length : float = Field(
        ..., ge=0 , description = "The length of the borrower’s employment in years."
    )
    annual_inc : float = Field(
        ..., ge=0 , description = "The borrower’s annual income."
    )
    dti : float = Field(
        ..., ge=0 , description = "Debt-to-income ratio, calculated as the borrower’s monthly debt payments divided by their monthly income."
    )
    loan_amnt : float = Field(
        ..., ge=0 , description = "why"
    )
    open_acc : float = Field(
        ..., ge=0 , description = "The number of open credit lines in the borrower’s credit history."
    )
    pub_rec : float = Field(
        ..., ge=0 , description = "The number of derogatory public records in the borrower’s credit history."
    )
    revol_bal : float = Field(
        ..., ge=0 , description = "The total credit revolving balance."
    )
    revol_util : float = Field(
        ..., ge=0 , description = "The revolving line utilization rate, or the amount of credit used relative to the total available credit."
    )
    total_acc : float = Field(
        ..., ge=0 , description = "The total number of credit accounts the borrower has."
    )
    collections_12_mths_ex_med : float = Field(
        ..., ge=0 , description = "The number of collections in the past 12 months, excluding medical collections."
    )
    
    mort_acc : float = Field(
        ..., ge=0 , description = "The number of mortgage accounts."
    )
    emp : float = Field(
        ..., ge=0 , description = "The borrower’s employer."
    )
    home_ownership : float = Field(
        ..., ge=0 , description = "The borrower’s home ownership status (e.g., rent, own, mortgage)."
    )
    #purpose : float = Field(
    #    ..., ge=0 , description = ' The purpose of the loan (e.g., debt consolidation, home improvement).'
    #)
    earliest_cr_line : float = Field(
        ..., ge=0 , description = "The date when the borrower’s earliest credit line was opened."
    )
    issue_d : float = Field(
        ..., ge=0 , description = "The date when the loan was issued."
    )

class Rating(BaseModel):
    loan_status: float = Field(
        ...,
        ge = 0 ,
        le = 10,
        description = "The current status of the loan (e.g., fully paid, charged off)."
    )

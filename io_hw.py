import pandas as pd
import seaborn as sns

def io_hw(out_path):
    
    df = pd.read_csv("NYC-RI.csv")  #The full pandas dataframe of the dataset
    
    head_df = df.head() #A new dataframe that is a copy of the first 5 lines of the dataframe, df
    
    head_df.to_csv(out_path)
    
    return df, head_df
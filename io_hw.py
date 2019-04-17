import pandas as pd
import seaborn as sns

def io_hw(out_path):
    '''
    This is your homework assignment.
    You will be wrting a function here.
    
    Your input will be:
    
    out_path: a string that is the path to output a csv of the head of your data.
    
    Your outputs will be:
    
    df: The full pandas dataframe of your dataset.
    head_df: A new dataframe that is a copy of the first 5 lines of your dataframe, df.
    '''
    df = pd.read_csv("https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv")
    
    head_df = df.head()
    head_df.to_csv(out_path,index = False)
    return df, head_df
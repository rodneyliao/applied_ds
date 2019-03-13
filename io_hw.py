import pandas as pd
import seaborn as sns
import pdb
import requests
import io

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
    url="https://s3.amazonaws.com/csvpastebin/uploads/c8ed3b2f0c9af99aaf21041dc2dafde1/salaries-by-college-type.csv"
    s=requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    head_df = df.head(5)
    head_df.to_csv(out_path)
    return df, head_df

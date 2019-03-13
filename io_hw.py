import pandas as pd
import seaborn as sns
import pdb
import csv

def io_hw(out_path):
    
    df= pd.read_csv('https://s3.amazonaws.com/csvpastebin/uploads/c8ed3b2f0c9af99aaf21041dc2dafde1/salaries-by-college-type.csv')
    head_df= df.head(5)
    head_df.to_csv(out_path)
    
    return df, head_df

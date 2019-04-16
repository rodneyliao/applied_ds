import pandas as pd
import seaborn as sns
import pdb
import csv

def io_hw(out_path):
    
    df= pd.read_csv('https://docs.google.com/spreadsheets/d/1cr65P3ciL2tD4W4KOCTz4Ik67iD52S_DKHXypqgta2o/export?format=csv')
    head_df= df.head(5)
    head_df.to_csv(out_path)

    return df, head_df
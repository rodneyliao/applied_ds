import pandas as pd
import seaborn as sns
import pdb
import csv
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
   
    ##df = pd.read_csv('https://www.kaggle.com/lava18/google-play-store-apps/downloads/googleplaystore.csv')
    ##df = pd.read_csv('./Data/googleplaystore.csv')
    df = pd.read_csv('https://tufts.box.com/shared/static/8utsdmfx97s0o1j63l1ogwr3822coo6l.csv')
    head_df = df.head(5)
    head_df.to_csv(out_path)

    return df, head_df


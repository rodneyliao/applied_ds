import pandas as pd
import seaborn as sns
import pdb
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
    url_teams = 'https://s3.amazonaws.com/csvpastebin/uploads/621900f3b91d9f7d8675e2b8768cf4a1/nflteams.csv'
    url_stadiums = 'https://s3.amazonaws.com/csvpastebin/uploads/9cbd92cc78c32f32136ff2fa7b75ff7b/nfl_stadiums.csv'
    url_scores = 'https://s3.amazonaws.com/csvpastebin/uploads/b8c5915cdf0a3d0cf0de55a86f77aa38/spreadspokescores.csv'
    
    df = pd.read_csv(url_teams)
    head_df = df.head(5)
    head_df.to_csv(out_path)
    
    return df, head_df

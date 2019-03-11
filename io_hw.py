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
    df = pd.read_excel('http://www.harpswell.maine.gov/vertical/Sites/%7B3F690C92-5208-4D62-BAFB-2559293F6CAE%7D/uploads/2018_COMMITMENT.xlsx')
    
    
    head_df = df.head()
    
    head_df.to_csv('./test.csv')

    return df, head_df

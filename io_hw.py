import pandas as pd
import seaborn as sns
import pdb

def io_hw(out_path):
    '''
    This is your homework assignment.
    You will be wrting a function here.
    
    Your input will be:
    
    out_path: a string that is the path to output a csv of the head of your data.
    
    You will load data, declare new variable for head, save head in out_path
    Your outputs will be:
    
    df: The full pandas dataframe of your dataset.
    head_df: A new dataframe that is a copy of the first 5 lines of your dataframe, df.
    pdb.set_trace()
    df = pd.read_csv('/Users/zhangdanhui/GoogleDrive/MSIM2018-2019/SP2019/EM212_Applied_Data_Science/Homework/Project_New_Seahorse/CellLineInput.csv')
    df = pd.read_csv('https://community.watsonanalytics.com/wp-content/uploads/2015/03/WA_Fn-UseC_-Operations-Dem-Planning_-BikeShare.csv')
    '''
    df = pd.read_csv('./CellLineInput.csv')
    
    head_df = df.head(5)
    head_df.to_csv(out_path)
    return df, head_df
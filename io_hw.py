import pandas as pd
import seaborn as sns

def io_hw(out_path):

    df = pd.read_csv('DavePyneData.csv')
    head_df = df.head()
    head_df.to_csv(out_path)
    return df, head_df

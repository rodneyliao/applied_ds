import pandas as pd
import seaborn as sns
import pdb
import csv

def io_hw(out_path):
    
    df= pd.read_csv('https://storage.googleapis.com/kaggle-datasets/1189/2137/salaries-by-college-type.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1552759212&Signature=H6sRA7fhcn%2FfveHHxAN624V%2F03iebFg1H2AMVYvjDPbtmFl1l4MbMyLKTObXat%2BeozkmiaISNZQtu3tb1%2BVkSqrxx2%2B7euoffugN%2BhxFJk%2F2Ti3YPA%2BWOVJrgRi0%2F0%2BDLs2pGRJCVzMqZP2HGjz5xdv3q%2BtShGWWWYNPVW68s%2F51oOlUlzk%2F6u7UTqYTlXehEeCmCiRDb8%2FGv9Y3SyzE4cmLoW%2FBdRwhE6IBLciVVrdGW4BRgBLLRbhlwmX9Y%2BK%2BONf%2BGrJWqcbYEgCEKcWl63OuBrCF%2BP2wGBH9Rtwp20%2FpICGU2FbcrlnJ6YcnDRVKMFMfZeRXR%2Ffom471Rtru6Q%3D%3D')
    head_df= df.head(5)
    head_df.to_csv(out_path)
    
    return df, head_df

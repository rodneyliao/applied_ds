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


   ##df = pd.read_csv('./Data/googleplaystore.csv')
   df = pd.read_csv('https://storage.googleapis.com/kaggle-datasets/14872/228180/Admission_Predict.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1552765636&Signature=N%2FPJ6QEQsW2KUFc1bNg35Aw%2B0jfIPkCVf3y%2FQgwun23HGyEcuPI0d2qadDy8iPkZVMLEdaytRPsn1CBmG9lqvPbdaKP1tdEizqC%2BymNerdPmmmMLQHOXcsxbrmaQV6nH8NSZSL6K%2BgFU849v6khW%2FJAD5zuFeod3MiqE4l0wXxqo44GCfrCKpYSE2eJIkIq2tPpMxHh12mTV7xb3qNXB4SasfRVPwCJdOCPYjQX7%2F5%2BTThzBgl4ryO1%2FEn3OVIr346QVm1%2FF8kfq1WWGH4NHCN7fsjUxVAs%2BQ7Moc1poUgT7AGiWm2sERJlre3ixECvYDpQnUxQXdLyLta%2Bhr8uj9g%3D%3D')
   head_df = df.head(5)
   head_df.to_csv(out_path)

   return df, head_df
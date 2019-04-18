import pandas as pd
import seaborn as sns
import numpy as np
import pytest
import eda_hw
import math

def get_data():
    dataset_df = sns.load_dataset('mpg').select_dtypes(include='number')
    return dataset_df.sample(axis=1).squeeze().dropna()

test_data = get_data()
print(test_data.head())

def test_average():
    """
    This function tests that you've implemented mean correctly
    """
    assert math.isclose(eda_hw.average(test_data), 
                        test_data.mean(), abs_tol=0.001)
    
def test_standard_deviation():
    assert math.isclose(eda_hw.standard_deviation(test_data),
                        test_data.std(ddof=0), abs_tol=0.001)

def test_median():
    assert eda_hw.median(test_data) == test_data.median()

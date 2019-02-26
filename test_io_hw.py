import pytest
import pandas as pd
import os
import io_hw

def test_io_hw():
    df, head_df = io_hw.io_hw('test.csv')
    assert (os.path.isfile('test.csv')), "file has not been saved"
    assert sum(1 for line in open('test.csv')) - 1 == len(head_df), 
    assert len(df.columns) == len(head_df.columns)
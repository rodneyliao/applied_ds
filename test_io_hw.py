import pytest
import pandas as pd
import os
import io_hw

name = 'elephant'

def test_io_hw():
    """
    This file grades the homework, io_hw.py
    It will check the following:
    - The function you wrote loads your dataset
    - The function you wrote saves first 5 rows your dataset
    """
    df, head_df = io_hw.io_hw('%s.csv' % name)
    assert os.path.isfile('%s.csv' % name)
    assert sum(1 for line in open('%s.csv' % name)) - 1 == len(head_df)
    assert len(df.columns) == len(head_df.columns)

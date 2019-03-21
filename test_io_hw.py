import pandas as pd
import numpy as np
import os
import pdb
import io_hw

num = np.random.randint(100000000)
name = 'elephant'

def test_io_hw():
    """
    This file grades the homework, io_hw.py
    It will check the following:
    - The function you wrote loads your dataset
    - The function you wrote saves first 5 rows your dataset
    """
    df, head_df = io_hw.io_hw('%s_%d.csv' % (name, num))
    assert os.path.isfile('%s_%d.csv' % (name, num))
    assert sum(1 for line in open('%s_%d.csv' % (name, num))) - 1 == len(head_df)
    assert len(df.columns) == len(head_df.columns)

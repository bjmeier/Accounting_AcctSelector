import pandas as pd
import numpy as np

def cleanDf(df_input, int_list):
    df = df_input.copy()
    df = df.fillna("")
    for c in int_list:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(np.int64)
    return df

import pandas as pd
import numpy as numpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
# import acquire

# ----------------- # 
#      Acquire      # 
# ----------------- #

def read_csv():
    sales = pd.read_csv("sales data-set.csv")

    store = pd.read_csv("stores data-set.csv")

    features = pd.read_csv("features data set.csv")

    return sales, store, features

def merge_df(sales, store, features):
    # Need to turn Date into a datetime df

    sales.Date = pd.to_datetime(sales.Date)
    features.Date = pd.to_datetime(features.Date)

    df = sales.merge(store, how="left", on="Store")
    df = df.merge(features, how="left", on=["Date", "Store"])

    df = df.set_index("Date")
    df = df.sort_index()
    return df

def fix_time_lag(df):
    new_df = pd.DataFrame()
    store_numbers = df.Store.unique()
    dept_numbers = df[df.Store == 4].Dept.unique()
    for store in store_numbers:

        for department in dept_numbers:
            df_debug = df[(df.Store == store) & (df.Dept == department)]
            df_debug = df_debug.groupby(df_debug.index).sum().resample("W").mean().ffill()
            new_df = pd.concat([df_debug, new_df])
    new_df = new_df.sort_index()
    return new_df

def wrangle_sales():
    sales, store, features = read_csv()

    df = merge_df(sales, store, features)

    # Impude markdown with zero

    df = df.fillna(0)

    df = fix_time_lag(df)

    return df

# ------------- #
#     Split     #
# ------------- #

def split_time_data_ptc(df, ptc):
    # Percentage-Based
    train_size = ptc
    n = df.shape[0]
    test_start_index = round(train_size * n)

    train = df[:test_start_index] # everything up (not including) to the test_start_index
    test = df[test_start_index:] # everything from the test_start_index to the end
    
    return train, test

def plot_splits(train, validate, test, target_variable):
    sns.lineplot(data=train, x=train.index, y= target_variable)
    sns.lineplot(data=validate, x=validate.index, y= target_variable)
    sns.lineplot(data=test, x=test.index, y= target_variable)




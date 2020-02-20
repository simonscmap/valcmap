""" Set of functions that validate data, dataset metadata and vars_metadata for CMAP standard format"""


"""
input: path, filename
output: none, or move file to vault/data/ and delete staging file

Large datasets will have metadata sheets seperate. Pass flag? 'data' page ignored
"""

import os
import pandas as pd
import sys
####################################


def validate_fpath(path, filename, opt_data_csv = None, split_data=False):
    assert os.path.isfile(path + filename), "File Path Not Found"
    assert filename.split('.')[-1] != 'xlsx'
    if split_data == True:
        assert os.path.isfile(path + opt_data_csv)
        df_data = pd.read_csv(path + opt_data_csv, sep=',')
        df_dataset_metadata = pd.read_excel(path + filename, sheet_name = 0)
        df_vars_metadata = pd.read_excel(path + filename, sheet_name = 1)
    else:
        df_data = pd.read_excel(path + filename, sheet_name = 0)
        df_dataset_metadata = pd.read_excel(path + filename, sheet_name = 1)
        df_vars_metadata = pd.read_excel(path + filename, sheet_name = 2)

    return df_data, df_dataset_metadata, df_vars_metadata


def validate_data(df):

    pass

def validate_dataset_metadata(df):
    pass

def valiate_vars_metadata(df):
    pass


def main(path, filename,opt_data_csv = None, split_data=False):
    df_data, df_dataset_metadata, df_vars_metadata = validate_fpath(path, filename,opt_data_csv,split_data)
    validate_data(df_data)
    validate_dataset_metadata(df_dataset_metadata)
    valiate_vars_metadata(df_vars_metadata)

path = os.getcwd()
filename = sys.argv[0]

main(path, filename,opt_data_csv = None, split_data=False)

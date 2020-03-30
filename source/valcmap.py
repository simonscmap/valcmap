## DEVNOTES 02-24-20
"""

Three main function types:

Validation functions:
    input: (dataframe, **, test name)
    output: dict with vals:
        test name
        error message
        any masked cols


"""
import pycmap
api = pycmap.API()
import os
import pandas as pd
import numpy as np
import sys
import csv
import datetime



##############################################################
###############                                ###############
#             Specalized/Single Use Functions                #
###############                                ###############
##############################################################

def validate_fpath(filename, opt_data_csv = None, split_data=False):
    assert os.path.isfile(filename), "File Path Not Found"
    assert filename.split('.')[-1] == 'xlsx'
    if split_data == True:
        assert os.path.isfile(opt_data_csv)
        df_data = pd.read_csv(opt_data_csv, sep=',')
        df_dataset_metadata = pd.read_excel(filename, sheet_name = 0)
        df_vars_metadata = pd.read_excel(filename, sheet_name = 1)
    else:
        df_data = pd.read_excel(filename, sheet_name = 0)
        df_dataset_metadata = pd.read_excel(filename, sheet_name = 1)
        df_vars_metadata = pd.read_excel(filename, sheet_name = 2)

    return df_data, df_dataset_metadata, df_vars_metadata


##############################################################
###############                                ###############
#                    Gereralized Functions                   #
###############                                ###############
##############################################################


# Check header columns
# Check Time format
# Check Latitude Format
# Check Longitude Format
# Check Depth Values are non Negative
# Check Missing Values
# Replace Missing Values with ''
# Sort By Time, Lat, Lon, Depth
# Dataset make - check if make.lower() is in tblMakes. If not, warn, pause to create new field in SQL server
# Column contains string, ex DOI



def col_name_validator(df,col_name_list, test_name):

    """ Validates the header names of a dataframe. Test function is named test_col_name_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
    Pandas dataframe containing column header names to be validated.
    col_name_list : list
    List of names for expected in header

    """

    header_name_list = list(df.columns)
    if set(header_name_list) == set(col_name_list):
        msg = column_name_msg
        non_matching_vals = ['']
    else:
        msg = 'WARNING: Column headers do not match input column list.'
        non_matching_vals = list(set(col_name_list) ^ set(header_name_list))

    col_name_validator_dict = {
        "test_name":test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return col_name_validator_dict

def length_validator(df, col, length,test_name, min_length='', suggested_max=''):

    """Validates a length limit for an input column. Test function is named: test_length_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be length validated.
    col : str
       Name of pandas dataframe column to validate.
    length : int
       Max length of values allowed in column.
    test_name : str
       Valdation test name.
    min_length (optional) : int
       Minimum length of string
    suggested_max : int
       Suggested Max -- if string length is greater then, will recomend to reduce length

    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            error message: str.
            masked_series: Pandas series of any values that are longer then length limit.
            mask: Pandas series of boolean mask. True == length invalid, False == length valid.

    """

    mask = (df[col].astype(str).str.len() >= int(length))
    masked_series = df[col][mask==True]
    if masked_series.empty:
        masked_series = ''
    if mask.any() == True:
        msg = 'WARNING: Some values are longer then accepted column limits. The character length limit for column: ' +  col + ' is: ' + str(length)  + ' Please modify your data and resubmit.'
    elif  min_length != '' and df[col].astype(str).str.len().any() >= int(suggested_max):
        msg += 'WARNING: Some values are longer then suggested length. The suggested character count for : ' +  col + ' is: ' + str(min_length)  + ' If you wish, reduce length.'
    elif min_length != '' and df[col].astype(str).str.len().any() < int(min_length):
        msg += 'WARNING: Some values are less then minimum length. Please modify and resubmit.'
    else:
        msg = ''

    length_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "masked_series": masked_series
        }

    return length_validator_dict



def time_format_validator(df, col, time_format,test_name):
    """Validates a time format for an input column. Test function is named: test_time_format_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be time format validated.
    col : str
       Name of pandas dataframe column to validate.
    time format : str
       Required time format
    test_name : str
       Valdation test name.


    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            test name: str - of test name for output dict
            error: str - error message
            non_matching_vals: List - any values in non agreement

    """
    try:
        datetime.datetime.strptime(df[col].astype(str)[0],time_format)
        msg = ''
        non_matching_vals = ''
    except:
        msg = 'WARNING: Time value does not match time format of: ' + time_format
        non_matching_vals = str(df[col].astype(str)[0])

    time_format_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return time_format_validator_dict

def make_list_validator(df, col,test_name):
    """Validates the dataset_make column to see if the value is in tblMakes in CMAP. Test function is named: test_make_list_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be time format validated.
    col : str
       Name of pandas dataframe column to validate.
    time format : str
       Required time format
    test_name : str
       Valdation test name.


    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            test name: str - of test name for output dict
            error: str - error message
            non_matching_vals: List - any values in non agreement

    """
    list_makes_cmap = list(api.query('''SELECT [make] FROM tblMakes''').iloc[:,0])
    list_makes_cmap_lowercase = [i.lower() for i in list_makes_cmap]
    if df[col].iloc[0] in list_makes_cmap_lowercase:
        msg = ''
        non_matching_vals = ''
    else:
        msg = str(df[col].iloc[0]) + ' is not a current option in the CMAP tblMakes. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_makes_cmap_lowercase)
        non_matching_vals = str(df[col].iloc[0])

    make_list_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return make_list_validator_dict

##############################################################
###############                                ###############
#               Validate Data Sheet Functions                #
###############                                ###############
##############################################################

def validate_data_time(df):
    length_validator(df, col, length)


def validate_data(df):
    validate_data_time()

##############################################################
###############                                ###############
#          Validate Dataset Metadata Sheet Functions         #
###############                                ###############
##############################################################

def dataset_short_name(df):
    dataset_short_name_length_validator_dict = length_validator(df, 'dataset_short_name', 50,'dataset metadata: validate short name length',1,30)
    return dataset_short_name_length_validator_dict

def dataset_long_name(df):
    dataset_long_name_length_validator_dict = length_validator(df, 'dataset_long_name',130,'dataset metadata: validate long name length',1,100)
    return dataset_long_name_length_validator_dict

def dataset_version(df):
    dataset_version_length_validator_dict = length_validator(df, 'dataset_version',50,'dataset metadata: validate version length',1,5)
    return dataset_version_length_validator_dict

def dataset_release_date(df):
    dataset_release_date_length_validator_dict = length_validator(df, 'dataset_release_date',50,'dataset metadata: validate release date length', 1,50)
    dataset_release_date_time_format_validator_dict = time_format_validator(df, 'dataset_release_date', '%Y-%m-%d','dataset metadata: validate release date time format')
    return dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict

def dataset_make(df):
    dataset_make_list_valdiator = make_list_validator(df, 'dataset_make','dataset metadata: validate dataset make')
    return dataset_make_list_valdiator

def validate_dataset_metadata(df):
    #sheet wide validation
    dataset_metadata_col_name_validator = col_name_validator(df,['dataset_short_name','dataset_long_name','dataset_version','dataset_release_date','dataset_make','dataset_source','dataset_distributor','dataset_acknowledgement','dataset_doi','dataset_history','dataset_description','dataset_references','climatology'], 'dataset metadata: validate column names')

    #column specific validation
    dataset_short_name_dict = dataset_short_name(df)
    dataset_long_name_dict = dataset_long_name(df)
    dataset_version_length_validator_dict = dataset_version(df)
    dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict = dataset_release_date(df)
    dataset_make_validator_dict = dataset_make(df)

    return dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict

def validate_vars_metadata(df):
    pass
##############################################################
###############                                ###############
#                    Compile Funcitons                       #
###############                                ###############
##############################################################



def write_to_csv(dict, fname):
    with open(fname,'a') as valoutput:
        wr = csv.writer(valoutput, quoting=csv.QUOTE_ALL)
        wr.writerow(list(dict.values()))


def compile_report(fname):
    write_to_csv(dataset_metadata_col_name_validator,fname)
    write_to_csv(dataset_short_name_dict,fname)
    write_to_csv(dataset_long_name_dict,fname)
    write_to_csv(dataset_version_length_validator_dict,fname)
    write_to_csv(dataset_release_date_length_validator_dict,fname)
    write_to_csv(dataset_release_date_time_format_validator_dict,fname)




def main(filename,opt_data_csv = None, split_data=False):
    df_data, df_dataset_metadata, df_vars_metadata = validate_fpath(filename,opt_data_csv,split_data)
    return df_data, df_dataset_metadata, df_vars_metadata
    # validate_data(df_data)
    # validate_dataset_metadata(df_dataset_metadata)
    # validate_vars_metadata(df_vars_metadata)


df_data, df_dataset_metadata, df_vars_metadata  = main('test_dataset.xlsx')

dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict = validate_dataset_metadata(df_dataset_metadata)


# compile_report('valcmap_output.csv')

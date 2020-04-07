## DEVNOTES 04-01-20
## -Eventually move all error messages into sql table to be shared between python and JS
## -Transition to command line tool, input is filepath --opts,
#export is filepath name with _validation appended. Print out any issues in error reportself.


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
from keyword import iskeyword



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


def col_name_validator(df,test_name,col_name_list):

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
        msg = ''
        non_matching_vals = ''
    else:
        msg = 'WARNING: Column headers do not match input column list.'
        non_matching_vals = sorted(set(set(col_name_list) ^ set(header_name_list)))

    col_name_validator_dict = {
        "test_name":test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return col_name_validator_dict

def length_validator(df, col,test_name, max_length = '', min_length='', suggested_max=''):

    """Validates a length limit for an input column. Test function is named: test_length_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be length validated.
    col : str
       Name of pandas dataframe column to validate.
    test_name : str
       Valdation test name.
    max_length (optinal) : int
       Maximum length of string
    min_length (optional) : int
       Minimum length of string
    suggested_max (optional) : int
       Suggested Max -- if string length is greater then, will recomend to reduce length

    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            error message: str.
            non_matching_vals: Pandas series of any values that are longer then length limit.
            mask: Pandas series of boolean mask. True == length invalid, False == length valid.

    """

    if max_length == '':
        max_len_mask = pd.Series(['False'] * len(df[col]))
    else:
        max_len_mask = (df[col].astype(str).str.len() >= int(max_length))

    if min_length == '':
        min_length_mask = pd.Series(['False'] * len(df[col]))
    else:
        min_length_mask = (df[col].astype(str).str.len() < int(min_length))

    if suggested_max == '':
        suggested_len_mask = pd.Series(['False'] * len(df[col]))
    else:
        suggested_len_mask = (df[col].astype(str).str.len() >= int(suggested_max))


    if max_len_mask.any() == True: # a True value exists in the series of masked max length
        msg = 'WARNING: Some values are longer then accepted column limits.'
        non_matching_vals = list(df[col][max_len_mask==True])

    elif min_length_mask.any() == True:
        msg = 'WARNING: Some values are less then minimum length.'
        non_matching_vals = list(df[col][min_length_mask==True])

    elif suggested_len_mask.any() == True:
        msg = 'WARNING: Some values are longer then suggested length.'
        non_matching_vals = list(df[col][suggested_len_mask==True])

    else:
        msg = ''
        non_matching_vals = ''


    length_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
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
    non_matching_vals = list(df[col][df[col].apply(lambda x: pd.to_datetime(x, errors='coerce', exact=True, format='%Y-%m-%d')).isnull()])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = 'WARNING: Time value(s) do not match time formats.'

    time_format_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return time_format_validator_dict

def climatology_bool_validator(df, col, test_name):
    """Validates the climatology column to check for 1 or null. Test function is named: test_climatology_bool_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be time format validated.
    col : str
       Name of pandas dataframe column to validate.
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
    if df[col].astype(str)[0] ==  '1' or df[col].astype(str)[0] ==  '0':
        msg = ''
        non_matching_vals = ''
    else:
        msg = 'WARNING: climatology values is not 0 or 1 (0 means dataset is not climatology product, 1 means dataset is climatology product.)'
        # print(msg)
        non_matching_vals = str(df[col].astype(str)[0])

    climatology_bool_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return climatology_bool_validator_dict





def make_list_validator(df, col,test_name):
    """Validates the dataset_make column to see if the value is in tblMakes in CMAP. Test function is named: test_time_format_validator() in test_valcmap.py.

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
        msg = 'The dataset Make input is not valid. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_makes_cmap_lowercase)
        non_matching_vals = str(df[col].iloc[0])

    make_list_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return make_list_validator_dict


def illegal_character_validator(df, col,test_name):

    """Checks a column for any illegal (for python variable names) characters. Test function is named: test_illegal_character_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be length validated.
    col : str
       Name of pandas dataframe column to validate.
    test_name : str
       Valdation test name.

    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            error message: str.
            msg: str
            non_matching_vals: List of any values that do not meet validation conditions.

    """

    def is_valid_variable_name(name):
        return name.isidentifier() and not iskeyword(name)

    non_matching_vals = list(df[col][~(df[col].apply(is_valid_variable_name))])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = "WARNING: illegal python variable names detected. var_short_names must be code friendly and cannot be reserved words. Names can contain lower and upper case ltters as well as numbers and underscores. They cannot begin with numbers or use special symbols such as: !, @, #, $, %. Some words are reserved in python. Those are: 'False','None','True','and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield'"

    illegal_character_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return illegal_character_validator_dict


##############################################################
###############                                ###############
#         Validate Dataset Metadata Sheet Functions          #
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
    dataset_short_name_length_validator_dict = length_validator(df, 'dataset_short_name','dataset metadata: validate short name length',50,1,30)
    return dataset_short_name_length_validator_dict

def dataset_long_name(df):
    dataset_long_name_length_validator_dict = length_validator(df, 'dataset_long_name','dataset metadata: validate long name length',130,1,100)
    return dataset_long_name_length_validator_dict

def dataset_version(df):
    dataset_version_length_validator_dict = length_validator(df, 'dataset_version','dataset metadata: validate version length',50,1,5)
    return dataset_version_length_validator_dict

def dataset_release_date(df):
    dataset_release_date_length_validator_dict = length_validator(df, 'dataset_release_date','dataset metadata: validate release date length',50,1,50)
    dataset_release_date_time_format_validator_dict = time_format_validator(df, 'dataset_release_date', '%Y-%m-%d','dataset metadata: validate release date time format')
    return dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict

def dataset_make(df):
    dataset_make_list_valdiator = make_list_validator(df, 'dataset_make','dataset metadata: validate dataset make')
    return dataset_make_list_valdiator

def dataset_source(df):
    dataset_source_length_validator = length_validator(df, 'dataset_source','dataset metadata: validate dataset source length',100,1)
    return dataset_source_length_validator

def dataset_distributor(df):
    dataset_distributor_length_validator = length_validator(df, 'dataset_distributor','dataset metadata: validate dataset distributor length',100)
    return dataset_distributor_length_validator

def dataset_acknowledgement(df):
    dataset_acknowledgement_length_validator = length_validator(df, 'dataset_acknowledgement','dataset metadata: validate dataset acknowledgement length',100,1)
    return dataset_acknowledgement_length_validator

def dataset_DOI(df):
    dataset_DOI_length_validator = length_validator(df, 'dataset_doi','dataset metadata: validate dataset DOI length',500)
    return dataset_DOI_length_validator

def dataset_history(df):
    dataset_history_length_validator = length_validator(df, 'dataset_history','dataset metadata: validate dataset history length',500)
    return dataset_history_length_validator

def dataset_description(df):
    dataset_description_length_validator = length_validator(df, 'dataset_description','dataset metadata: validate dataset description length',10000,50) #max, min , suggested max
    return dataset_description_length_validator

def dataset_references(df):
    dataset_references_length_validator = length_validator(df, 'dataset_references','dataset metadata: validate dataset reference length', 500)
    return dataset_references_length_validator

def dataset_climatology(df):
    dataset_climatology_length_validator = length_validator(df, 'climatology','dataset metadata: validate dataset climatology length',2)
    dataset_climatology_bool_check_validator = climatology_bool_validator(df, 'climatology', 'dataset metadata: validate dataset climatology bool values')
    return dataset_climatology_length_validator, dataset_climatology_bool_check_validator

###################################################

def validate_dataset_metadata(df):
    #sheet wide validation
    dataset_metadata_col_name_validator = col_name_validator(df, 'dataset metadata: validate column names',['dataset_short_name','dataset_long_name','dataset_version','dataset_release_date','dataset_make','dataset_source','dataset_distributor','dataset_acknowledgement','dataset_doi','dataset_history','dataset_description','dataset_references','climatology'])

    #column specific validation
    dataset_short_name_dict = dataset_short_name(df)
    dataset_long_name_dict = dataset_long_name(df)
    dataset_version_length_validator_dict = dataset_version(df)
    dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict = dataset_release_date(df)
    dataset_make_validator_dict = dataset_make(df)
    dataset_source_valdiator_dict = dataset_source(df)
    dataset_distributor_validator_dict = dataset_distributor(df)
    dataset_acknowledgement_valdator_dict = dataset_acknowledgement(df)
    dataset_DOI_validator_dict =  dataset_DOI(df)
    dataset_history_validator_dict = dataset_history(df)
    dataset_desciption_validator_dict = dataset_description(df)
    dataset_references_validator_dict = dataset_references(df)
    dataset_climatology_length_validator_dict, dataset_climatology_bool_check_validator_dict = dataset_climatology(df)

    return dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict, dataset_source_valdiator_dict, dataset_distributor_validator_dict, dataset_acknowledgement_valdator_dict, dataset_DOI_validator_dict, dataset_history_validator_dict, dataset_desciption_validator_dict, dataset_references_validator_dict, dataset_climatology_length_validator_dict, dataset_climatology_bool_check_validator_dict


##############################################################
###############                                ###############
#         Validate Dataset Metadata Sheet Functions          #
###############                                ###############
##############################################################

#var_short_name
#< variable short name (<50 chars) >  ↓ Validate length, illegal python chars including spaces, match vars in datasheet
def var_short_name(df):
    dataset_short_name_length_validator_dict = length_validator(df, 'dataset_short_name','dataset metadata: validate short name length',50,1,30)
    return dataset_short_name_length_validator_dict

#var_long_name
#< variable short name (<50 chars) >  ↓ Validate length
def var_long_name(df):
    var_long_name_length_validator_dict = length_validator(df, 'var_long_name','vars metadata: validate long name length',200,1,100)
    return var_long_name_length_validator_dict


##############################################################

def validate_vars_metadata(df):

    #sheet wide validation

    #column specific validation

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
    dataset_metadata_list = [dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict, dataset_source_valdiator_dict, dataset_distributor_validator_dict, dataset_acknowledgement_valdator_dict, dataset_DOI_validator_dict, dataset_history_validator_dict, dataset_desciption_validator_dict, dataset_references_validator_dict, dataset_climatology_length_validator_dict, dataset_climatology_bool_check_validator_dict]
    for check in dataset_metadata_list:
        write_to_csv(check,fname)





def main(filename,opt_data_csv = None, split_data=False):
    df_data, df_dataset_metadata, df_vars_metadata = validate_fpath(filename,opt_data_csv,split_data)
    return df_data, df_dataset_metadata, df_vars_metadata
    validate_data(df_data)
    validate_dataset_metadata(df_dataset_metadata)
    validate_vars_metadata(df_vars_metadata)


# df_data, df_dataset_metadata, df_vars_metadata  = main('test_dataset.xlsx')
# # #
# dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict, dataset_source_valdiator_dict, dataset_distributor_validator_dict, dataset_acknowledgement_valdator_dict, dataset_DOI_validator_dict, dataset_history_validator_dict, dataset_desciption_validator_dict, dataset_references_validator_dict, dataset_climatology_length_validator_dict, dataset_climatology_bool_check_validator_dict = validate_dataset_metadata(df_dataset_metadata)
#
# #
# compile_report('valcmap_output.csv')

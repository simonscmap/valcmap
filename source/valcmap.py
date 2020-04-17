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

def length_validator(df, col,test_name, max_length = '', min_length='', suggested_max='', delimit_str_flag = False, delimiter = ''):

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
    delimit_str_flag (optional) : bool
       If True, column string will be split by delimiter and count will be based on # of strings, not total string length. ie. keywords.
    delimiter (optional) : str
       Delimiter to seperated strings if delimit_str_flag = True. ex: ','

    Returns
    -------
    length_validator_dict : dictionary
        python dictionary containing:
            error message: str.
            non_matching_vals: Pandas series of any values that are longer then length limit.
            mask: Pandas series of boolean mask. True == length invalid, False == length valid.

    """
    if delimit_str_flag == True:
        column_string_length = df[col].astype(str).str.split(str(delimiter)).str.len()
    else:
        column_string_length = df[col].astype(str).str.len()

    if max_length == '':
        max_len_mask = pd.Series(['False'] * len(df[col]))
    else:
        max_len_mask = (column_string_length >= int(max_length))

    if min_length == '':
        min_length_mask = pd.Series(['False'] * len(df[col]))
    else:
        min_length_mask = (column_string_length < int(min_length))

    if suggested_max == '':
        suggested_len_mask = pd.Series(['False'] * len(df[col]))
    else:
        suggested_len_mask = (column_string_length >= int(suggested_max))


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

def lat_format_validator(df, col,test_name):
    """Validates a lat format for an input column. Test function is named: test_lat_format_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be lat format validated.
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
    lat_dtype_check = str(df[col].dtype) == 'float64' or str(df[col].dtype) == 'int64'

    if lat_dtype_check == True:
        lat_max_check = (df[col] > 90.0).any()
        lat_min_check = (df[col] < -90).any()
    else:
        lat_max_check = False
        lat_min_check = False

    non_matching_vals = ''
    msg = ''
    if lat_dtype_check == False:
        msg += ' Latitude values are not all floats, perhaps the lats are not in decimal degrees.'
    if lat_max_check == True:
        msg += ' One or more latitude values are larger than 90. This exceeds the decimal latitude range.'
    if lat_min_check == True:
        msg += ' One or more latitude values are lower than -90. This exceeds the decimal latitude range.'


    lat_format_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return lat_format_validator_dict

def lon_format_validator(df, col,test_name):
    """Validates a lon format for an input column. Test function is named: test_lon_format_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be lon format validated.
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
    lon_dtype_check = str(df[col].dtype) == 'float64' or str(df[col].dtype) == 'int64'
    if lon_dtype_check == True:
        lon_max_check = (df[col] > 180.0).any()
        lon_min_check = (df[col] < -180).any()

    else:
        lon_max_check = False
        lon_min_check = False

    non_matching_vals = ''
    msg = ''
    if lon_dtype_check == False:
        msg += '  Longitude values are not all floats, perhaps the lons are not in decimal degrees.  '
    if lon_max_check == True:
        msg += '  One or more longitude values are larger than 90. This exceeds the decimal longitude range.  '
    if lon_min_check == True:
        msg += '  One or more longitude values are lower than -90. This exceeds the decimal longitude range.  '


    lon_format_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return lon_format_validator_dict

def depth_format_validator(df, col,test_name):
    """Validates a depth format for an input column. Test function is named: test_depth_format_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be depth format validated.
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
    depth_dtype_check = str(df[col].dtype) == 'float64' or str(df[col].dtype) == 'int64'

    if depth_dtype_check == True:
        depth_sign_check = (df[col] >= 0).any()
        depth_max_physical_check = (df[col] < 11000.0).any() #depth of Mariana Trench
    else:
        depth_sign_check = False
        depth_max_physical_check = False

    non_matching_vals = ''
    msg = ''
    if depth_dtype_check == False:
        msg += ' Depth values are not all floats or ints, perhaps the depths have invalid formatting.'
    if depth_sign_check == True:
        msg += ' One or more depth values are less than 0. Depth values are a positive # in meters.'
    if depth_max_physical_check == True:
        msg += ' One or more depth values are larger than 11000. Did you find somewhere deeper than the Mariana Trench? If not, are your depth values formatted in meters?'


    depth_format_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }

    return depth_format_validator_dict

def climatology_bool_validator(df, col, test_name):
    """Validates the climatology column to check for 1 or null. Test function is named: test_climatology_bool_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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
       Pandas dataframe containing column to be validated.
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

def var_sensor_validator(df, col,test_name):
    """Validates the var_sensor column to see if the value is in tblSensors in CMAP. Test function is named: test_var_sensor_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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
    list_sensor_cmap = list(api.query('''SELECT [Sensor] FROM tblSensors''').iloc[:,0])
    list_sensor_cmap_lowercase = [i.lower() for i in list_sensor_cmap]

    non_matching_vals = list(df[col][~df[col].str.lower().isin(list_sensor_cmap_lowercase)])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = 'The var_sensor input is not valid. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_sensor_cmap_lowercase)


    var_sensor_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return var_sensor_validator_dict

def var_spatial_res_validator(df, col,test_name):
    """Validates the var_spatial_res column to see if the value is in tblSpatial_Resolutions in CMAP. Test function is named: test_var_spatial_res_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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
    list_spatial_res_cmap = list(api.query('''SELECT [Spatial_Resolution] FROM tblSpatial_Resolutions''').iloc[:,0])
    list_spatial_res_lowercase = [i.lower() for i in list_spatial_res_cmap]
    list_spatial_res_lowercase = [ch.replace('â', '') for ch in list_spatial_res_lowercase]

    non_matching_vals = list(df[col][~df[col].str.lower().isin(list_spatial_res_lowercase)])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = 'The var_spatial_res input is not valid. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_spatial_res_lowercase)


    var_spatial_res_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return var_spatial_res_validator_dict

def var_temporal_res_validator(df, col,test_name):
    """Validates the var_temporal_res column to see if the value is in tbltemporal_Resolutions in CMAP. Test function is named: test_var_temporal_res_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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
    list_temporal_res_cmap = list(api.query('''SELECT [Temporal_Resolution] FROM tblTemporal_Resolutions''').iloc[:,0])
    list_temporal_res_lowercase = [i.lower() for i in list_temporal_res_cmap]
    print(list_temporal_res_lowercase)
    non_matching_vals = list(df[col][~df[col].str.lower().isin(list_temporal_res_lowercase)])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = 'The var_temporal_res input is not valid. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_temporal_res_lowercase)


    var_temporal_res_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return var_temporal_res_validator_dict


def var_discipline_validator(df, col,test_name):
    """Validates the var_discipline column to see if the value is in tblStudy_Domains in CMAP. Test function is named: test_var_discipline_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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
    list_var_discipline_cmap = list(api.query('''SELECT [Study_Domain] FROM tblStudy_Domains''').iloc[:,0])
    list_var_discipline_lowercase = [i.lower() for i in list_var_discipline_cmap]
    print(list_var_discipline_lowercase)
    non_matching_vals = list(df[col][~df[col].str.lower().isin(list_var_discipline_lowercase)])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = 'The var_discipline input is not valid. Please contact the CMAP team and we can add other options. The current options are: ' + str(list_var_discipline_lowercase)


    var_discipline_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return var_discipline_validator_dict

def visualize_validator(df, col,test_name):

    """Validates the visualize column to see if the value is 0,1 or null. Test function is named: test_visualize_validator() in test_valcmap.py.

    Parameters
    ----------
    df : pandas dataframe
       Pandas dataframe containing column to be validated.
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

    non_matching_vals = list(df[col][~df[col].str.lower().isin(['0','1'])])

    if not non_matching_vals: #if the non matching vals list is empty...
        non_matching_vals = ''
        msg = ''
    else:
        msg = "The visualize input contains invalid values. 0 or 1  are the only acceptable inputs. (0 means variable is not meant to be visualized in the CMAP web application, 1 means the variable is meant to be visualized in the CMAP web application.)"


    visualize_validator_dict = {
        "test_name": test_name,
        "error": msg,
        "non_matching_vals": non_matching_vals
        }
    return visualize_validator_dict




##############################################################
###############                                ###############
#                 Validate Data Sheet Functions              #
###############                                ###############
##############################################################


"""
-Does header contain minimum, time,lat,lon columns. if contains depth..
-Do columns that != time,lat,lon,depth match vars_metadata_columns?
-Are columns in time, lat, lon...depth .
    ie,
        if column_list contains depth:
            mask column list expected w/ column list[0:4]
        else:
            column list expected w/ column list[0:3]

column time - time validator
lat - check range -90,90. Are all vals float or int. (no degree bs)
lon - check range -180,180. Are all vals float or int.


Data
Check header cols (time, lat, lon, depth?) - does depth exist. - do non, ST vars match vars_metadata variables?
Is the order of cols in time,lat,lon,<depth>...
Check time, lat, lon, depth formatting
time: Format  %Y-%m-%dT%H:%M:%S,  Time-Zone:  UTC,
Lat: Decimal (not military grid system), Unit: degree, Range: [-90, 90]
Lon: Decimal (not military grid system), Unit: degree, Range: [-180, 180]
Depth: Positive value, Unit: [m]
"""

def data_time(df):
    data_time_fmt_val = time_format_validator(df, 'time', '%Y-%m-%dT%H:%M:%S','data: validate time col time format')
    return data_time_fmt_val

def data_lat(df):
    data_lat_fmt_val = lat_format_validator(df,'lat','data: validate lat col format')
    return data_lat_fmt_val

def data_lon(df):
    data_lon_fmt_val = lon_format_validator(df,'lon','data: validate lon col format')
    return data_lon_fmt_val

def data_depth(df):
    data_depth_fmt_val = depth_format_validator(df,'depth','data: validate depth col format')
    return data_depth_fmt_val


def ds_col_validator(df_data, df_vars_metadata):
    vm_cols = list(df_vars_metadata)
    if 'depth' in list(df_data):
        ds_col_val = col_name_validator(df_data, 'dataset: validate column names match var names. w/ depth',list(df_data[4:]))
    else:
        ds_col_val = col_name_validator(df_data, 'dataset: validate column names match var names. w/o depth',list(df_data[3:]))
    return ds_col_val


def validate_data(df):
    #sheet wide validation
    ds_col_val = ds_col_validator(df_data, df_vars_metadata)
    #column specific validation
    data_time_fmt_val = data_time(df)
    data_lat_fmt_val = data_lat(df)
    data_lon_fmt_val = data_lon(df)
    data_depth_fmt_val = data_depth(df)
    return ds_col_val, data_time_fmt_val, data_lat_fmt_val, data_lon_fmt_val, data_depth_fmt_val

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
#          Validate Dataset Metadata Sheet Functions         #
###############                                ###############
##############################################################
def dataset_short_name(df):
    dataset_short_name_length_validator_dict = length_validator(df, 'dataset_short_name','vars metadata: validate short name length',50,1,30)
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
#            Validate Vars Metadata Sheet Functions          #
###############                                ###############
##############################################################


def var_short_name(df):
    vm_short_name_lv = length_validator(df, 'dataset_short_name','dataset metadata: validate short name length',50,1,30)
    vm_short_name_ic = illegal_character_validator(df, 'dataset_short_name','vars metadata: validate short name illegal chars.')
    return vm_short_name_lv, vm_short_name_ic

def var_long_name(df):
    vm_long_name_lv= length_validator(df, 'var_long_name','vars metadata: validate long name length',200,1,100)
    return vm_long_name_lv

def var_sensor(df):
    vm_sensor = var_sensor_validator(df, 'var_sensor','vars metadata: validate var_sensor')
    return vm_sensor

def var_unit(df):
    vm_unit_len = length_validator(df, 'var_unit','vars metadata: validate unit length',50)
    return vm_unit_len

def var_spatial_res(df):
    vm_spatial = var_spatial_res_validator(df, 'var_spatial_res','vars metadata: validate var_spatial_res')
    return vm_spatial

def var_temporal_res(df):
    vm_temporal =var_temporal_res_validator(df, 'var_temporal_res','vars metadata: validate var_temporal_res')
    return vm_temporal

def var_discipline(df):
    vm_dis = var_discipline_validator(df, 'var_discipline','vars metadata: validate var_discipline')
    return vm_dis

def visualize(df):
    vm_vis = visualize_validator(df, 'visualize','vars metadata: validate visualize')
    return vm_vis

def keywords(df):
    vm_kw_len = length_validator(df, 'var_keywords','keyword', max_length = '', min_length=5, suggested_max='', delimit_str_flag = True, delimiter = ',')
    return vm_kw_len
##############################################################

def validate_vars_metadata(df):

    #sheet wide validation
    vm_col_name = col_name_validator(df, 'vars metadata: validate column names',['var_short_name','var_long_name','var_sensor','var_unit','var_spatial_res','var_temporal_res','var_missing_value','var_discipline','visualize','var_keywords','var_comment'])

    #column specific validation
    vm_short_name_lv, vm_short_name_ic = var_short_name(df)
    vm_long_name_lv = var_long_name(df)
    vm_sensor = var_sensor(df)
    vm_unit_len = var_unit(df)
    vm_spatial = var_spatial_res(df)
    vm_temporal = var_temporal_res(df)
    vm_dis = var_discipline(df)
    vm_vis = visualize(df)
    vm_kw_len = keywords(df)

    return vm_col_name, vm_short_name_lv, vm_short_name_ic, vm_long_name_lv, vm_sensor, vm_unit_len, vm_spatial, vm_temporal,vm_dis, vm_vis, vm_kw_len

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



# dataset_metadata_col_name_validator,dataset_short_name_dict,dataset_long_name_dict,dataset_version_length_validator_dict,dataset_release_date_length_validator_dict, dataset_release_date_time_format_validator_dict, dataset_make_validator_dict, dataset_source_valdiator_dict, dataset_distributor_validator_dict, dataset_acknowledgement_valdator_dict, dataset_DOI_validator_dict, dataset_history_validator_dict, dataset_desciption_validator_dict, dataset_references_validator_dict, dataset_climatology_length_validator_dict, dataset_climatology_bool_check_validator_dict = validate_dataset_metadata(df_dataset_metadata)
#
# #
# compile_report('valcmap_output.csv')

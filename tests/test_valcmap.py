import pandas as pd
import sys

sys.path.append('../source')
import valcmap



def test_col_name_validator():
    #df,col_name_list, test_name
    test_name = 'column name validator test'
    col_name_list = ['dataset_short_name','dataset_long_name','dataset_version','dataset_release_date','dataset_make','dataset_source','dataset_distributor','dataset_acknowledgement','dataset_doi','dataset_history','dataset_description','dataset_references','climatology']
    df_pass = pd.DataFrame(columns = ['dataset_short_name','dataset_long_name','dataset_version','dataset_release_date','dataset_make','dataset_source','dataset_distributor','dataset_acknowledgement','dataset_doi','dataset_history','dataset_description','dataset_references','climatology'])
    df_fail = pd.DataFrame(columns = ['dataset_short_name','dataset_long_name','dataset_release_date','dataset_make','dataset_source','dataset_distributor','dataset_acknowledgement','dataset_doi','dataset_history','dataset_description'])

    """expected outputs"""
    col_name_pass_expected = {"test_name": 'column name validator test', "error": '',"non_matching_vals": ['']}
    col_name_fail_expected = {"test_name": 'column name validator test', "error": 'WARNING: Column headers do not match input column list.',"non_matching_vals": sorted(set(['dataset_version','dataset_references','climatology']))}


    """func calls"""
    col_name_pass = valcmap.col_name_validator(df_pass, test_name,col_name_list)
    col_name_fail = valcmap.col_name_validator(df_fail, test_name,col_name_list)


    """tests"""
    assert col_name_pass == col_name_pass_expected, "col name pass test passed..."
    assert col_name_fail == col_name_fail_expected, "col name fail test passed..."
    return col_name_fail, col_name_fail_expected


def test_length_validator():


    test_name = 'length validator test'
    df = pd.DataFrame({'max_length': ['000000','00000'],
                       'min_length': ['2', '200'],
                       'suggested_max': ['33333','300000']})

    """expected outputs"""
    max_length_pass_expected = {"test_name": 'length validator test', "error": '',"non_matching_vals": ''}
    max_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are longer then accepted column limits.',"non_matching_vals": ['000000']}
    min_length_pass_expected = {"test_name": 'length validator test', "error": '',"non_matching_vals": ''}
    min_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are less then minimum length.',"non_matching_vals": ['2']}
    suggested_max_length_pass_expected = {"test_name": 'length validator test', "error": '',"non_matching_vals": ''}
    suggested_max_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are longer then suggested length.',"non_matching_vals": ['300000']}

    """func calls"""
    max_length_pass = valcmap.length_validator(df, 'max_length', test_name, max_length = 7, min_length='', suggested_max='')
    max_length_fail = valcmap.length_validator(df, 'max_length', test_name, max_length = 6, min_length='', suggested_max='')
    min_length_pass = valcmap.length_validator(df, 'min_length', test_name, max_length = '', min_length=1, suggested_max='')
    min_length_fail = valcmap.length_validator(df, 'min_length', test_name, max_length = '', min_length=2, suggested_max='')
    suggested_max_length_pass = valcmap.length_validator(df, 'suggested_max', test_name, max_length = '', min_length='', suggested_max=7)
    suggested_max_length_fail = valcmap.length_validator(df, 'suggested_max', test_name, max_length = '', min_length='', suggested_max=6)


    """tests"""
    assert max_length_pass == max_length_pass_expected, "max length pass test failed..."
    assert max_length_fail == max_length_fail_expected, "max length fail test failed..."
    assert min_length_pass == min_length_pass_expected, "min length pass test failed..."
    assert min_length_fail == min_length_fail_expected, "min length fail test failed..."
    assert suggested_max_length_pass == suggested_max_length_pass_expected, "suggested max pass test failed..."
    assert suggested_max_length_fail == suggested_max_length_fail_expected, "suggested max fail test failed..."

def test_time_format_validator():

    test_name = 'time format validator test'
    df = pd.DataFrame({'pass_time_format_yymmdd': ['2000-01-01','2010-01-01'],
                       'fail_time_format_yymmdd': ['2000 / 01 / 01', 'APR122010'],
                       'pass_time_format_yymmddThhmmss': ['2000-01-01T12:01:01','2010-01-01T12:01:01'],
                       'fail_time_format_yymmddThhmmss': ['2000 / 01 / 01 / 12:01:01','12APR2020']})

    """expected outputs"""
    pass_time_format_yymmdd_expected = {"test_name": 'time format validator test', "error": '',"non_matching_vals": ['']}
    fail_time_format_yymmdd_expected = {"test_name": 'time format validator test', "error": 'WARNING: Time value(s) do not match time formats.',"non_matching_vals": ['2000 / 01 / 01', 'APR122010']}
    pass_time_format_yymmddThhmmss_expected = {"test_name": 'time format validator test', "error": '',"non_matching_vals": ['']}
    fail_time_format_yymmddThhmmss_expected = {"test_name": 'time format validator test', "error": 'WARNING: Time value(s) do not match time formats.',"non_matching_vals": ['2000 / 01 / 01 / 12:01:01','12APR2020']}

    """func calls"""
    pass_time_format_yymmdd        = valcmap.time_format_validator(df, 'pass_time_format_yymmdd', '%Y-%m-%d',test_name)
    fail_time_format_yymmdd        = valcmap.time_format_validator(df, 'fail_time_format_yymmdd', '%Y-%m-%d',test_name)
    pass_time_format_yymmddThhmmss = valcmap.time_format_validator(df, 'pass_time_format_yymmddThhmmss', '%Y-%m-%dT%H:%M:%S',test_name)
    fail_time_format_yymmddThhmmss = valcmap.time_format_validator(df, 'fail_time_format_yymmddThhmmss', '%Y-%m-%dT%H:%M:%S',test_name)

    """tests"""
    # return pass_time_format_yymmdd, pass_time_format_yymmdd_expected
    assert pass_time_format_yymmdd == pass_time_format_yymmdd_expected, "pass time format yymmdd failed..."
    assert fail_time_format_yymmdd == fail_time_format_yymmdd_expected, "fail time format yymmdd failed..."
    assert pass_time_format_yymmddThhmmss == pass_time_format_yymmddThhmmss_expected, "pass time format yymmddThhmmss failed..."
    assert fail_time_format_yymmddThhmmss == fail_time_format_yymmddThhmmss_expected, "fail time format yymmddThhmmss failed..."


def test_climatology_bool_validator():

    test_name = 'climatology boolean test'

    df = pd.DataFrame({'pass_climatology_0': ['0'],
                       'pass_climatology_1': ['1'],
                       'fail_climatology': ['climatology']})

    """expected outputs"""
    pass_climatology_0_expected = {"test_name": 'climatology boolean test', "error": '',"non_matching_vals": ''}
    pass_climatology_1_expected = {"test_name": 'climatology boolean test', "error": '',"non_matching_vals": ''}
    fail_climatology_expected   = {"test_name": 'climatology boolean test', "error": 'WARNING: climatology values is not 0 or 1 (0 means dataset is not climatology product, 1 means dataset is climatology product.)',"non_matching_vals": 'climatology'}

    """func calls"""
    pass_climatology_0 = valcmap.climatology_bool_validator(df, 'pass_climatology_0',test_name)
    pass_climatology_1 = valcmap.climatology_bool_validator(df, 'pass_climatology_1',test_name)
    fail_climatology   = valcmap.climatology_bool_validator(df, 'fail_climatology',test_name)

    """tests"""
    assert pass_climatology_0 == pass_climatology_0_expected, "pass climatology 0 bool failed..."
    assert pass_climatology_1 == pass_climatology_1_expected, "pass climatology 1 bool failed..."
    assert fail_climatology   == fail_climatology_expected, "fail climatology test failed..."

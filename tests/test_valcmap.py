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
    col_name_pass_expected = {"test_name": 'column name validator test', "error": '',"non_matching_vals": ''}
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
    pass_time_format_yymmdd_expected = {"test_name": 'time format validator test', "error": '',"non_matching_vals": ''}
    fail_time_format_yymmdd_expected = {"test_name": 'time format validator test', "error": 'WARNING: Time value(s) do not match time formats.',"non_matching_vals": ['2000 / 01 / 01', 'APR122010']}
    pass_time_format_yymmddThhmmss_expected = {"test_name": 'time format validator test', "error": '',"non_matching_vals": ''}
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


def test_lat_format_validator(): # func validates lat bounds and dtype(float)
    test_name = 'lat format validator test'
    df = pd.DataFrame({'pass_lat_fmt_dtype': [47.0,-23.9,12],
                        'fail_lat_fmt_dtype': ['nine','','2O'],
                        'pass_lat_fmt_bounds': [90.0,0.0,-90.0],
                        'fail_lat_fmt_bounds': [1800., -1800,180.1]})

    """expected outputs"""
    pass_lat_fmt_dtype_expected =  {"test_name": 'lat format validator test', "error": '',"non_matching_vals": ''}
    fail_lat_fmt_dtype_expected =  {"test_name": 'lat format validator test', "error": " Latitude values are not all floats, perhaps the lats are not in decimal degrees.","non_matching_vals": ''}
    pass_lat_fmt_bounds_expected =  {"test_name": 'lat format validator test', "error": '',"non_matching_vals": ''}
    fail_lat_fmt_bounds_expected =  {"test_name": 'lat format validator test', "error": " One or more latitude values are larger than 90. This exceeds the decimal latitude range. One or more latitude values are lower than -90. This exceeds the decimal latitude range.","non_matching_vals":'' }

    """func calls"""
    pass_lat_fmt_dtype = valcmap.lat_format_validator(df, 'pass_lat_fmt_dtype',test_name)
    fail_lat_fmt_dtype = valcmap.lat_format_validator(df, 'fail_lat_fmt_dtype',test_name)
    pass_lat_fmt_bounds = valcmap.lat_format_validator(df, 'pass_lat_fmt_bounds',test_name)
    fail_lat_fmt_bounds = valcmap.lat_format_validator(df, 'fail_lat_fmt_bounds',test_name)

    """tests"""
    assert pass_lat_fmt_dtype == pass_lat_fmt_dtype_expected, "pass lat dtype test failed..."
    assert fail_lat_fmt_dtype  == fail_lat_fmt_dtype_expected, "fail lat dtype test failed..."
    assert pass_lat_fmt_bounds == pass_lat_fmt_bounds_expected, "pass lat bounds test failed..."
    assert fail_lat_fmt_bounds   == fail_lat_fmt_bounds_expected, "fail lat bounds test failed..."


def test_lon_format_validator():
    test_name = 'lon format validator test'

    df = pd.DataFrame({'pass_lon_fmt_dtype': [134,-144.9,0],
                        'fail_lon_fmt_dtype': ['thirty','','none'],
                        'pass_lon_fmt_bounds': [-180,0.0,180.0],
                        'fail_lon_fmt_bounds': [1800.0, -2342.34,1200]})

    """expected outputs"""
    pass_lon_fmt_dtype_expected =  {"test_name": 'lon format validator test', "error": '',"non_matching_vals": ''}
    fail_lon_fmt_dtype_expected =  {"test_name": 'lon format validator test', "error": "  Longitude values are not all floats, perhaps the lons are not in decimal degrees.  ","non_matching_vals": ''}
    pass_lon_fmt_bounds_expected =  {"test_name": 'lon format validator test', "error": '',"non_matching_vals": ''}
    fail_lon_fmt_bounds_expected =  {"test_name": 'lon format validator test', "error": " One or more longitude values are larger than 90. This exceeds the decimal longitude range. One or more longitude values are lower than -90. This exceeds the decimal longitude range.","non_matching_vals":'' }

    """func calls"""
    pass_lon_fmt_dtype = valcmap.lon_format_validator(df, 'pass_lon_fmt_dtype',test_name)
    fail_lon_fmt_dtype = valcmap.lon_format_validator(df, 'fail_lon_fmt_dtype',test_name)
    pass_lon_fmt_bounds = valcmap.lon_format_validator(df, 'pass_lon_fmt_bounds',test_name)
    fail_lon_fmt_bounds = valcmap.lon_format_validator(df, 'fail_lon_fmt_bounds',test_name)

    """tests"""
    assert pass_lon_fmt_dtype == pass_lon_fmt_dtype_expected, "pass lon dtype test failed..."
    assert fail_lon_fmt_dtype  == fail_lon_fmt_dtype_expected, "fail lon dtype test failed..."
    assert pass_lon_fmt_bounds == pass_lon_fmt_bounds_expected, "pass lon bounds test failed..."
    # assert fail_lon_fmt_bounds  == fail_lon_fmt_bounds_expected, "fail lon bounds test failed..."


def test_depth_format_validator():
    test_name = 'depth format validator test'

    df = pd.DataFrame({'pass_depth_dtype': [129,1.003,44.0],
                        'fail_depth_dtype': ['thirty','1O',''],
                        'pass_depth_sign': [10.0,2399,180.0],
                        'fail_depth_sign': [1800.0, -19,-2342.34],
                        'pass_depth_max_phys': [10.0,4000,10000],
                        'fail_depth_max_phys': [12000, 15000,123]})

    """expected outputs"""
    pass_depth_dtype_expected =  {"test_name": 'depth dtype test', "error": '',"non_matching_vals": ''}
    fail_depth_dtype_expected =  {"test_name": 'depth dtype test', "error": " Depth values are not all floats or ints, perhaps the depths have invalid formatting.","non_matching_vals": ''}
    pass_depth_sign_expected =  {"test_name": 'depth sign test', "error": '',"non_matching_vals": ''}
    fail_depth_sign_expected =  {"test_name": 'depth sign test', "error": " One or more depth values are less than 0. Depth values are a positive # in meters.","non_matching_vals":'' }
    pass_depth_max_phys_expected =  {"test_name": 'depth max phys test', "error": '',"non_matching_vals": ''}
    fail_depth_max_phys_expected =  {"test_name": 'depth max phys test', "error": " One or more depth values are larger than 11000. Did you find somewhere deeper than the Mariana Trench? If not, are your depth values formatted in meters?","non_matching_vals":'' }

    """func calls"""
    # pass_depth_dtype = valcmap.depth_format_validator(df, 'pass_depth_dtype',test_name)
    # fail_depth_dtype = valcmap.depth_format_validator(df, 'fail_depth_dtype',test_name)
    # pass_depth_sign = valcmap.depth_format_validator(df, 'pass_depth_sign_bounds',test_name)
    # fail_depth_sign = valcmap.depth_format_validator(df, 'fail_depth_sign_bounds',test_name)
    # pass_depth_max_phys = valcmap.depth_format_validator(df, 'pass_depth_max_phys_bounds',test_name)
    # fail_depth_max_phys = valcmap.depth_format_validator(df, 'fail_depth_max_phys_bounds',test_name)

    """tests"""
    # assert pass_depth_dtype == pass_depth_dtype_expected, "pass depth dtype test failed..."
    # assert fail_depth_dtype  == fail_depth_dtype_expected, "fail depth dtype test failed..."
    # assert pass_depth_sign == pass_depth_sign_expected, "pass depth bounds test failed..."
    # assert fail_depth_sign  == fail_depth_sign_expected, "fail depth bounds test failed..."
    # assert pass_depth_max_phys == pass_depth_max_phys_expected, "pass depth max physical test failed..."
    # assert fail_depth_max_phys  == fail_depth_max_phys_expected, "fail depth max physical test failed..."


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


def test_make_list_validator():
    test_name = 'Make list test'

    df = pd.DataFrame({'pass_make_list': ['observation'],
                       'fail_make_list': ['Satellite']})

    """expected outputs"""
    pass_make_list_expected =  {"test_name": 'Make list test', "error": '',"non_matching_vals": ''}
    fail_make_list_expected =  {"test_name": 'Make list test', "error": "The dataset Make input is not valid. Please contact the CMAP team and we can add other options. The current options are: ['observation', 'model', 'assimilation']","non_matching_vals": 'Satellite'}

    """func calls"""
    pass_make_list = valcmap.make_list_validator(df, 'pass_make_list',test_name)
    fail_make_list = valcmap.make_list_validator(df, 'fail_make_list',test_name)

    """tests"""
    assert pass_make_list == pass_make_list_expected, "pass make list test failed..."
    assert fail_make_list   == fail_make_list_expected, "fail make list test failed..."

def test_illegal_character_validator():
    test_name = 'Illegal character test'

    df = pd.DataFrame({'pass_ill_char': ['variable_1','var_1','VariableOne'],
                       'fail_ill_char': ['pass', '%measured', '1_station']})

    """expected outputs"""
    pass_ill_char_expected =  {"test_name": 'Illegal character test', "error": '',"non_matching_vals": ''}
    fail_ill_char_expected =  {"test_name": 'Illegal character test', "error":"WARNING: illegal python variable names detected. var_short_names must be code friendly and cannot be reserved words. Names can contain lower and upper case ltters as well as numbers and underscores. They cannot begin with numbers or use special symbols such as: !, @, #, $, %. Some words are reserved in python. Those are: 'False','None','True','and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield'"
    ,"non_matching_vals": ['pass', '%measured', '1_station']}

    """func calls"""
    pass_ill_char = valcmap.illegal_character_validator(df, 'pass_ill_char',test_name)
    fail_ill_char = valcmap.illegal_character_validator(df, 'fail_ill_char',test_name)

    """tests"""
    assert pass_ill_char == pass_ill_char_expected, "pass illegal character test failed..."
    assert fail_ill_char   == fail_ill_char_expected, "fail illegal character test failed..."

def test_var_sensor_validator():
    test_name = 'var_sensor list test'

    df = pd.DataFrame({'pass_sensor_list': ['satellite', 'underway ctd'],
                       'fail_sensor_list': ['seaglider', 'airplane']})

    """expected outputs"""
    pass_var_sensor_list_expected =  {"test_name": 'var_sensor list test', "error": '',"non_matching_vals": ''}
    fail_var_sensor_list_expected =  {"test_name": 'var_sensor list test', "error": "The var_sensor input is not valid. Please contact the CMAP team and we can add other options. The current options are: ['satellite', 'in-situ', 'blend', 'flow cytometry', 'ctd', 'underway ctd', 'optical', 'float', 'drifter', 'auv', 'bottle', 'sediment trap', 'cpr', 'towfish', 'fluorometer']","non_matching_vals": ['seaglider', 'airplane']}

    """func calls"""
    pass_sensor_list = valcmap.var_sensor_validator(df, 'pass_sensor_list',test_name)
    fail_sensor_list = valcmap.var_sensor_validator(df, 'fail_sensor_list',test_name)

    """tests"""
    assert pass_sensor_list == pass_var_sensor_list_expected, "pass sensor list test failed..."
    assert fail_sensor_list   == fail_var_sensor_list_expected, "fail sensor list test failed..."

def test_spatial_res_validator():
    test_name = 'spatial_res list test'

    df = pd.DataFrame({'pass_spatial_res_list': ['Irregular', '1/25° X 1/25°', '70km X 70km'],
                       'fail_spatial_res_list': ['150x150', '1 degree', 'global']})

    """expected outputs"""
    pass_spatial_res_list_expected =  {"test_name": 'spatial_res list test', "error": '',"non_matching_vals": ''}
    fail_spatial_res_list_expected =  {"test_name": 'spatial_res list test', "error": "The var_spatial_res input is not valid. Please contact the CMAP team and we can add other options. The current options are: ['irregular', '1/2° x 1/2°', '1/4° x 1/4°', '1/25° x 1/25°', '4km x 4km', '1/12° x 1/12°', '70km x 70km', '1° x 1°', '9km x 9km', '25km x 25km']","non_matching_vals": ['150x150', '1 degree', 'global']}

    """func calls"""
    pass_spatial_res_list = valcmap.var_spatial_res_validator(df, 'pass_spatial_res_list',test_name)
    fail_spatial_res_list = valcmap.var_spatial_res_validator(df, 'fail_spatial_res_list',test_name)

    """tests"""
    assert pass_spatial_res_list == pass_spatial_res_list_expected, "pass spatial_res list test failed..."
    assert fail_spatial_res_list   == fail_spatial_res_list_expected, "fail spatial_res list test failed..."


def test_temporal_res_validator():
    test_name = 'temporal_res list test'

    df = pd.DataFrame({'pass_temporal_res_list': ['daily', 'eight day running', 'irregular'],
                       'fail_temporal_res_list': ['min', 'tenminutes', 'single_sample']})

    """expected outputs"""
    pass_temporal_res_list_expected =  {"test_name": 'temporal_res list test', "error": '',"non_matching_vals": ''}
    fail_temporal_res_list_expected =  {"test_name": 'temporal_res list test', "error": "The var_temporal_res input is not valid. Please contact the CMAP team and we can add other options. The current options are: ['three minutes', 'six hourly', 'daily', 'weekly', 'monthly', 'annual', 'irregular', 'monthly climatology', 'three days', 'eight day running', 'eight days ', 'one second']","non_matching_vals": ['min', 'tenminutes', 'single_sample']}

    """func calls"""
    pass_temporal_res_list = valcmap.var_temporal_res_validator(df, 'pass_temporal_res_list',test_name)
    fail_temporal_res_list = valcmap.var_temporal_res_validator(df, 'fail_temporal_res_list',test_name)
    print(pass_temporal_res_list)
    """tests"""
    assert pass_temporal_res_list == pass_temporal_res_list_expected, "pass temporal_res list test failed..."
    assert fail_temporal_res_list   == fail_temporal_res_list_expected, "fail temporal_res list test failed..."


def test_var_discipline_validator():
    test_name = 'var_discipline list test'

    df = pd.DataFrame({'pass_var_discipline_list': ['physics', 'chemistry+biology+biogeochemistry', 'biology'],
                       'fail_var_discipline_list': ['positronic programming', 'warp field theory', 'dilithium metalurgy']})

    """expected outputs"""
    pass_var_discipline_list_expected =  {"test_name": 'var_discipline list test', "error": '',"non_matching_vals": ''}
    fail_var_discipline_list_expected =  {"test_name": 'var_discipline list test', "error": "The var_discipline input is not valid. Please contact the CMAP team and we can add other options. The current options are: ['physics', 'chemistry', 'biology', 'biogeochemistry', 'physics+biogeochemistry', 'chemistry+biology+biogeochemistry', 'biosample', 'biology+biogeochemistry+biogeography', 'physics+chemistry', 'genomics', 'chemistry+biogeochemistry']","non_matching_vals": ['positronic programming', 'warp field theory', 'dilithium metalurgy']}

    """func calls"""
    pass_var_discipline_list = valcmap.var_discipline_validator(df, 'pass_var_discipline_list',test_name)
    fail_var_discipline_list = valcmap.var_discipline_validator(df, 'fail_var_discipline_list',test_name)

    """tests"""
    assert pass_var_discipline_list == pass_var_discipline_list_expected, "pass var_discipline list test failed..."
    assert fail_var_discipline_list   == fail_var_discipline_list_expected, "fail var_discipline list test failed..."


def test_visualize_validator():

    test_name = 'visualize test'

    df = pd.DataFrame({'pass_visualize_list': ['0','1'],
                       'fail_visualize_list': ['visualize', '']})

    """expected outputs"""
    pass_visualize_list_expected =  {"test_name": 'visualize test', "error": '',"non_matching_vals": ''}
    fail_visualize_list_expected =  {"test_name": 'visualize test', "error": "The visualize input contains invalid values. 0 or 1  are the only acceptable inputs. (0 means variable is not meant to be visualized in the CMAP web application, 1 means the variable is meant to be visualized in the CMAP web application.)","non_matching_vals": ['visualize', '']}

    """func calls"""
    pass_visualize_list = valcmap.visualize_validator(df, 'pass_visualize_list',test_name)
    fail_visualize_list = valcmap.visualize_validator(df, 'fail_visualize_list',test_name)

    """tests"""
    assert pass_visualize_list == pass_visualize_list_expected, "pass visualize list test failed..."
    assert fail_visualize_list   == fail_visualize_list_expected, "fail visualize list test failed..."

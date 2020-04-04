import pandas as pd
import sys

sys.path.append('../source')
import valcmap


def test_length_validator():
    """
    test conditions, pass and throw messages:
    len larger then max length
    len less then min length
    len larger then suggested length
    test multiple row returns, ie func should catch if one val passes and one fails.
    """
    test_name = 'length validator test'
    df = pd.DataFrame({'max_length': ['000000','00000'],
                       'min_length': ['2', '200'],
                       'suggested_max': ['33333','300000']})

    #expected outputs"""
    max_length_pass_expected = {"test_name": 'length validator test', "error": '',"masked_series": ''}
    max_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are longer then accepted column limits.',"masked_series": ['000000']}

    min_length_pass_expected = {"test_name": 'length validator test', "error": '',"masked_series": ''}
    min_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are less then minimum length.',"masked_series": ['2']}

    suggested_max_length_pass_expected = {"test_name": 'length validator test', "error": '',"masked_series": ''}
    suggested_max_length_fail_expected = {"test_name": 'length validator test', "error": 'WARNING: Some values are longer then suggested length.',"masked_series": ['300000']}

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

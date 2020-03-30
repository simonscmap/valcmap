import pandas as pd
import sys

sys.path.append('../source')
import valcmap


def test_length_validator():


    df = pd.DataFrame({'col1': [123, 'aaaaaaaaaaaa', 11,55555,'bbbbb'], 'col2': ['three', 4, '22', '4', 7777]})
    expected_mask = pd.Series([False, True, False, True, True])
    expected_series_mask = pd.Series(['aaaaaaaaaaaa', 55555, 'bbbbb'])
    col = 'col1'
    length = '5'

    length_validator_dict = valcmap.length_validator(df, col, length)
    assert length_validator_dict['mask'].equals(expected_mask) == True, "length validator mask does not match expected mask"
    assert list(length_validator_dict['masked_series']) == list(expected_series_mask), "masked series does not match expected masked_series"

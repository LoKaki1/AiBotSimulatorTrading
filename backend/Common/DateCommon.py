import datetime as dt
import pandas as pd
from typing import Union

from pandas import DatetimeIndex


def generate_dates_between_two_dates(start_date: Union[str, dt.datetime],
                                      end_data: Union[str, dt.datetime]) -> DatetimeIndex:
    return pd.date_range(start_date, end_data)


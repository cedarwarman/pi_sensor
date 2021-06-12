#!/usr/bin/env python3

import datetime as DT
import argparse
import pandas as pd
from gspread_pandas import Spread

### Trim sheet
def trim_sheet(days, sheet_id):
    # Setting dates
    current_date = pd.Timestamp('today').floor('D')
    start_date = current_date - pd.Timedelta(days, unit='D')
    print(current_date)
    print(start_date)

    # Opening a spreadsheet
    input_sheet = Spread(sheet_id)

    # Converting to dataframe
    df = input_sheet.sheet_to_df(index=None)
    print(df)

    # Converting date column to datetime type
    df.loc[:,'date'] = pd.to_datetime(df.loc[:,'date'], format='%Y-%m-%d')

    # Subsetting dataframe to past x days
    df = df[(df['date'] > start_date) & (df['date'] <= current_date)]
    print(df)


### Main
def main():
    trim_sheet(7, '15Ak9f5qAX8dY5QKb9ZHiYEmtQF3dSgMBgc1LH5VKRwM')


if __name__ == "__main__":
    main()

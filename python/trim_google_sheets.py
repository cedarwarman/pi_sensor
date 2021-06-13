#!/usr/bin/env python3

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

    # Converting back to string for upload (the apostrophe is for google sheets
    # to not convert it back to a date, because this breaks the R script).
    df.loc[:,'date'] = "'" + df.loc[:,'date'].dt.strftime('%Y-%m-%d')

    # Adding apostrophe to time for google sheets

    df.loc[:,'time'] = "'" + df.loc[:,'time']

    print(df.dtypes)

    # Uploading the new sheet
    input_sheet.df_to_sheet(df, 
        index=False, 
        replace=True)

#def update_sheet(input_df)

### Main
def main():
    trim_sheet(7, '15Ak9f5qAX8dY5QKb9ZHiYEmtQF3dSgMBgc1LH5VKRwM')


if __name__ == "__main__":
    main()

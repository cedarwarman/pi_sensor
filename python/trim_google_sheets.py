#!/usr/bin/env python3

import time
#import gspread
import argparse
import pandas as pd
from gspread_pandas import Spread

# Opening a spreadsheet
input_sheet = Spread('15Ak9f5qAX8dY5QKb9ZHiYEmtQF3dSgMBgc1LH5VKRwM')

# Converting to dataframe
df = input_sheet.sheet_to_df(index=None)

print("the spreadsheet:")
print(df)
#print(df.dtypes)
#print(df.iloc[:, 0])

# Testing conversion of date column to datetime type
date_column = df.loc[:,'date']
print("Date column:")
print(date_column)
print("Converted to time object:")
print(pd.to_datetime(date_column, format='%Y-%m-%d'))

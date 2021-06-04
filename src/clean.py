import logging.config

import pandas as pd


logger = logging.getLogger(__name__)


def yards_to_miles(df, column_name, digits):
    df[column_name] = round(df[column_name] / 1760, digits)
    return df


def df_drop_str(df, column_name, drop_str):
    df_drop = df[~df[column_name].str.lower().str.contains(drop_str)]
    return df_drop


def clean(raw_data_path, length_col, digits, name_col, drop_str, clean_path):
    df = pd.read_csv(raw_data_path)
    df_clean = yards_to_miles(df, length_col, digits)
    df_clean = df_drop_str(df_clean, name_col, drop_str)

    df_clean.to_csv(clean_path, index=False)
    logger.info('Cleaned dataframe saved.')

    return df_clean

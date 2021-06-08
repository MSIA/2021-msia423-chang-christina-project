import logging.config

import pandas as pd

logger = logging.getLogger(__name__)


def yards_to_miles(df, column_name, digits):
    """Converts the units of a dataframe column from yards to miles.

        Args:
            df (:obj:`pandas.DataFrame`): dataframe with a column for a
            distance measure
            column_name (str): name of column with distance measure
            digits (int): number of places to round

        Returns:
            df (:obj:`pandas.DataFrame`): dataframe where the specified column
            is converted from yards to miles
    """

    # Divide yards by 1760 to get miles
    df[column_name] = round(df[column_name] / 1760, digits)
    return df


def df_drop_str(df, column_name, drop_str):
    """Drop dataframe rows that contain a specific string.

        Args:
            df (:obj:`pandas.DataFrame`): dataframe with a string column
            column_name (str): name of string column
            drop_str (int): string to drop

        Returns:
            df (:obj:`pandas.DataFrame`): dataframe where rows were dropped
            if they contained drop_str
    """
    df_drop = df[~df[column_name].str.lower().str.contains(drop_str)]
    return df_drop


def clean(raw_data_path, length_col, digits, name_col, drop_str, clean_path):
    """Create cleaned dataframe and save to specified path.

        Args:
            raw_data_path (str): path to cleaned data file
            length_col (str): name of column with distance measure
            digits (int): number of places to round
            name_col (str): name of string column
            drop_str (int): string to drop
            clean_path (str): location to save cleaned dataframe

        Returns:
            df (:obj:`pandas.DataFrame`): cleaned dataframe
    """
    df = pd.read_csv(raw_data_path)
    df_clean = yards_to_miles(df, length_col, digits)
    df_clean = df_drop_str(df_clean, name_col, drop_str)

    df_clean.to_csv(clean_path, index=False)
    logger.info('Cleaned dataframe saved.')

    return df_clean

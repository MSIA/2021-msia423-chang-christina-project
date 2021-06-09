import logging.config

import numpy as np
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
    try:
        df[column_name] = round(df[column_name] / 1760, digits)
        logger.info("Successfully converted yards to miles for %s", column_name)
        return df
    except KeyError as e:
        logger.info("Could not convert %s from yards to miles", column_name)
        logger.error("Please make sure the column_name is in the dataframe")
    except TypeError as e:
        logger.info("Could not convert %s from yards to miles", column_name)
        logger.error("Please make sure inputs have correct types")


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
    df_rows = np.shape(df)[0]

    # Drop rows that contain the drop str in the specified column
    try:
        df_drop = df[~df[column_name].str.lower().str.contains(drop_str)]
    except KeyError as e:
        logger.info("Could not convert %s from yards to miles", column_name)
        logger.error("Please make sure the column_name is in the dataframe")
    except TypeError as e:
        logger.info("Could not convert %s from yards to miles", column_name)
        logger.error("Please make sure inputs have correct types")

    df_rows_drop = np.shape(df_drop)[0]

    # Log how many rows were dropped
    num_dropped = df_rows - df_rows_drop

    if num_dropped != 0:
        logger.warning("Dropped %s rows from the data", num_dropped)

    logger.info("The data has %s rows after filtering the drop string",
                np.shape(df_drop)[0])

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
    try:
        df = pd.read_csv(raw_data_path)
        logger.debug("File successfully read")
    except FileNotFoundError as e:
        logger.error("File could not be found. Please make sure the path is"
                     "correct.")

    # Convert yards to miles and filter the rows
    df_clean = yards_to_miles(df, length_col, digits)
    df_clean = df_drop_str(df_clean, name_col, drop_str)

    df_clean.to_csv(clean_path, index=False)
    logger.info('Cleaned dataframe saved.')

    return df_clean

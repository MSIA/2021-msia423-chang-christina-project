import logging.config

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def one_hot_encode(df, trail_id, tag_features, non_tag_features, response):
    # Get column names of categorical and numerical variables
    df_features = df[non_tag_features]
    cat_names = df_features.select_dtypes(include='object').columns
    num_names = df_features.select_dtypes(include=np.number).columns

    # Encode categorical variables
    enc_columns = pd.get_dummies(df_features[cat_names], drop_first=True)
    enc_columns.columns = [i.replace(' ', '_') for i in enc_columns.columns]

    # Concatenate encoded columns to numerical columns, and tag features
    df_enc = pd.concat([df[trail_id], df_features[num_names], enc_columns, df[tag_features], df[response]], axis=1)

    return df_enc


def list_to_text(ls, path):
    textfile = open(path, "w")
    for element in ls:
        textfile.write(element + "\n")
    textfile.close()


def expand_column(df, column_name, path):
    """"""
    # Clean and split the elements by comma
    split_series = [i.strip('[]') for i in df[column_name]]
    split_series = pd.Series([i.replace("\'", "").replace("-", "_").split(', ') for i in split_series])

    # Save the column's unique values
    column_list = list(split_series)
    flat_list = [item for sublist in column_list for item in sublist]
    flat_list = [x for x in flat_list if x != '']
    unique_val = np.unique(flat_list)
    list_to_text(unique_val, path)

    # Create dummy dataframe
    df_split = split_series.str.join('|').str.get_dummies()
    df_split.columns = column_name + '_' + df_split.columns

    # Join dummies with dataframe
    df_expand = df.join(df_split)

    # Drop original column
    df_expand = df_expand.drop(columns=column_name)

    return df_expand


def bin_feature(df, cut_labels, cut_bins, num_col_name, bin_col_name):
    """
    cut_labels (list)
    cut_bins (list)
    """
    df[bin_col_name] = pd.cut(df[num_col_name], bins=cut_bins, labels=cut_labels)
    df.drop(columns=num_col_name, inplace=True)

    return df


def featurize(clean_data_path, trail_id, tag_features, non_tag_features, response,
              features_name, features_ls_path,
              activities_name, activities_ls_path,
              cut_labels, cut_bins, num_col_name, bin_col_name,
              featurize_path):

    # Read in cleaned data
    df = pd.read_csv(clean_data_path)

    # Select features and one hot encode non-tag categorical variables
    df_ohe = one_hot_encode(df, trail_id, tag_features, non_tag_features, response)

    # Create dummy variable for each tag
    df_expand = expand_column(df_ohe, features_name, features_ls_path)
    df_expand = expand_column(df_expand, activities_name, activities_ls_path)

    # Create response variable
    df_featurize = bin_feature(df_expand, cut_labels, cut_bins, num_col_name, bin_col_name)

    # Save df
    df_featurize.to_csv(featurize_path, index=False)
    logger.info('Featurize dataframe saved.')

    return df_featurize


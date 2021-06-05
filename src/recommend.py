import logging.config

import numpy as np
import pandas as pd
import pickle
import re

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
logger = logging.getLogger(__name__)


def input_tag_ohe(feature_name, full_tag_ls, tag_input):
    # feature_name: name of feature to append to column
    # full_tag_ls: entire list of unique tags
    # tag_input: list of tag inputs

    split_series = pd.Series([full_tag_ls, tag_input])
    df_split = split_series.str.join('|').str.get_dummies()
    df_split.columns = feature_name + '_' + df_split.columns
    tag_ohe = df_split.iloc[1, :]

    return tag_ohe


def column_ohe(df, column_name, col_input):
    # returns series
    full_value_ls = list(df[column_name].unique())
    full_value_ls = [i.replace(' ', '_') for i in full_value_ls]
    split_series = pd.Series([full_value_ls, [col_input]])
    df_split = split_series.str.join('|').str.get_dummies()
    df_split.columns = column_name + '_' + df_split.columns

    # Drop column for first unique value
    ohe_res = df_split.iloc[1, 1:]
    return ohe_res


def collect_input(length_input, elevation_gain_input, route_type_input, features_input, activities_input):

    # Convert string with brackets to list
    features_input = re.findall(r'\'\s*([^\']*?)\s*\'', features_input)
    activities_input = re.findall(r'\'\s*([^\']*?)\s*\'', activities_input)

    # Create input dictionary
    input_dict = {'length': length_input,
                  'elevation_gain': elevation_gain_input,
                  'route_type': route_type_input,
                  'features': features_input,
                  'activities': activities_input}

    return input_dict


def create_input_features(features_name, full_features_ls,
                          activities_name, full_activities_ls,
                          df, route_type,
                          input_dict):
    # returns pandas.core.series.Series

    length_input = input_dict['length']
    elevation_gain_input = input_dict['elevation_gain']
    route_type_input = input_dict['route_type']
    features_input = input_dict['features']
    activities_input = input_dict['activities']

    # One hot encode tags and categorical variable
    features_ohe = input_tag_ohe(features_name, full_features_ls, features_input)
    activities_ohe = input_tag_ohe(activities_name, full_activities_ls, activities_input)
    route_type_ohe = column_ohe(df, route_type, route_type_input)

    # Numerical inputs
    num_features = pd.Series({'length': length_input, 'elevation_gain': elevation_gain_input})

    # Create input vector
    input_vector = pd.concat([num_features, route_type_ohe, features_ohe, activities_ohe])

    return input_vector


def scaled_cosine_sim(df):
    # Standard scaling for numerical data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Calculate distance
    cs = cosine_similarity(df_scaled)

    return cs


def recommend_trails(n, df_features, df, trail_id, response, input_vector, display_feature_list):
    # df_features: one hot encoded
    # df: includes trail info

    # Set trail_id to be the index
    input_matrix = df_features.set_index(trail_id)
    input_matrix = input_matrix.drop(columns=[response])

    # Save trail ids to reference for recommendation
    input_matrix_ind = input_matrix.index

    # Insert new input in first row, use this to calculate similarity
    input_dist = pd.concat([pd.DataFrame(input_vector).transpose(), input_matrix])

    # Calculate distance
    cs = scaled_cosine_sim(input_dist)

    # Get similarities for the new input
    sim_vec = cs[0, :]

    # Get the n largest similarities
    sim_ind = sim_vec.argsort()[-(n + 1):][::-1][1:]

    # Get the trail id using the index
    most_sim_id = list(input_matrix_ind[sim_ind])
    # most_sim_df = df[df[trail_id].isin(most_sim_id)].reset_index(drop=True)
    #
    # # Show a subset of columns
    # res = most_sim_df[display_feature_list]

    return most_sim_id


def predict_difficulty(input_vector, model_path):
    # Make prediction
    input_arr = np.array(input_vector).reshape(1, -1)
    model = pickle.load(open(model_path, 'rb'))
    # pred = pd.Series({response: model.predict(input_arr)[0]})
    pred = model.predict(input_arr)[0]

    return pred


def predict(length_input, elevation_gain_input, route_type_input, features_input, activities_input,
            features_name, full_features_ls_path, activities_name, full_activities_ls_path, clean_data_path, route_type,
            model_path):

    df = pd.read_csv(clean_data_path)

    with open(full_features_ls_path) as f:
        full_features_ls = [line.rstrip() for line in f]

    with open(full_activities_ls_path) as f:
        full_activities_ls = [line.rstrip() for line in f]

    dict_input = collect_input(length_input, elevation_gain_input, route_type_input, features_input, activities_input)
    user_input = create_input_features(features_name, full_features_ls,
                                       activities_name, full_activities_ls,
                                       df, route_type,
                                       dict_input)

    return predict_difficulty(user_input, model_path)


def recommend(length_input, elevation_gain_input, route_type_input, features_input, activities_input,
              features_name, full_features_ls_path, activities_name, full_activities_ls_path, clean_data_path,
              route_type, n, featurize_path, trail_id, response, display_feature_list):

    df = pd.read_csv(clean_data_path)
    df_features = pd.read_csv(featurize_path)

    with open(full_features_ls_path) as f:
        full_features_ls = [line.rstrip() for line in f]

    with open(full_activities_ls_path) as f:
        full_activities_ls = [line.rstrip() for line in f]

    dict_input = collect_input(length_input, elevation_gain_input, route_type_input, features_input, activities_input)
    user_input = create_input_features(features_name, full_features_ls,
                                       activities_name, full_activities_ls,
                                       df, route_type,
                                       dict_input)

    return recommend_trails(n, df_features, df, trail_id, response, user_input, display_feature_list)
    #recommend_trails(5, df_featurize, df, 'trail_id', 'difficulty_class', user_input, display_feature_list)

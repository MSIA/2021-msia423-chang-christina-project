import logging.config
import pickle
import re

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def input_tag_ohe(feature_name, full_tag_ls, tag_input):
    """One hot encode tags of user input.

        Args:
            feature_name (str): name of feature to append to column
            full_tag_ls (:obj:`list` of :obj:`str`): full list of unique tags
            tag_input (:obj:`list` of :obj:`str`): list of tag inputs

        Returns:
            Series of one hot encoded input tag

    """

    # One hot encode user input
    split_series = pd.Series([full_tag_ls, tag_input])
    df_split = split_series.str.join('|').str.get_dummies()

    # Append to column name
    df_split.columns = feature_name + '_' + df_split.columns
    tag_ohe = df_split.iloc[1, :]
    logger.debug("User input for %s successfully one hot encoded", feature_name)

    return tag_ohe


def column_ohe(df, column_name, col_input):
    """One hot encode categorical feature.

        Args:
            df (:obj:`pandas.DataFrame`): dataframe with categorical feature
            column_name (str): name of categorical feature
            col_input (str): input of the user for the feature

        Returns:
            Series of one hot encoded values from the user input

    """
    # Returns series for one hot encoded values
    try:
        full_value_ls = list(df[column_name].unique())
    except KeyError as e:
        logger.error("Please make sure %s is in the dataframe", column_name)
    full_value_ls = [i.replace(' ', '_') for i in full_value_ls]
    split_series = pd.Series([full_value_ls, [col_input]])
    df_split = split_series.str.join('|').str.get_dummies()
    df_split.columns = column_name + '_' + df_split.columns

    # Drop column for first unique value
    ohe_res = df_split.iloc[1, 1:]
    logger.info("User input for %s successfully one hot encoded", column_name)

    return ohe_res


def collect_input(length_input, elevation_gain_input, route_type_input,
                  features_input, activities_input):
    """Reformat the user input into a dictionary.

        Args:
            length_input (str):  user input for length
            elevation_gain_input (str): user input for elevation gain
            route_type_input (str): user input for route type
            features_input (str): user input for features
            activities_input (str): user input for activities

        Returns:
            Dictionary of user inputs

    """

    # Convert string with brackets to list
    features_input = re.findall(r'\'\s*([^\']*?)\s*\'', features_input)
    activities_input = re.findall(r'\'\s*([^\']*?)\s*\'', activities_input)

    # Create input dictionary
    input_dict = {'length': length_input,
                  'elevation_gain': elevation_gain_input,
                  'route_type': route_type_input,
                  'features': features_input,
                  'activities': activities_input}
    logger.debug("User input converted to dictionary")

    return input_dict


def create_input_features(features_name, full_features_ls,
                          activities_name, full_activities_ls,
                          df, route_type,
                          input_dict):
    """Convert user input into a feature vector.

        Args:
            features_name (str): name of tag feature
            full_features_ls (:obj:`list` of :obj:`str`): full list of unique
            tags for features
            activities_name (str): name of activities feature
            full_activities_ls (:obj:`list` of :obj:`str`): full list of unique
            tags for activities
            df (:obj:`pandas.DataFrame`): cleaned dataframe
            route_type (str): name of route type column
            input_dict: (:obj: `dict`): dictionary of user inputs

        Returns:
            Series of user inputs

    """

    # Collect the user inputs
    length_input = input_dict['length']
    elevation_gain_input = input_dict['elevation_gain']
    route_type_input = input_dict['route_type']
    features_input = input_dict['features']
    activities_input = input_dict['activities']

    # One hot encode tags and categorical variable
    features_ohe = input_tag_ohe(features_name, full_features_ls,
                                 features_input)
    activities_ohe = input_tag_ohe(activities_name, full_activities_ls,
                                   activities_input)
    route_type_ohe = column_ohe(df, route_type, route_type_input)
    logger.info("All tags and categorical features successfully one hot"
                "encoded")

    # Numerical inputs
    num_features = pd.Series({'length': length_input,
                              'elevation_gain': elevation_gain_input})

    # Create input vector
    input_vector = pd.concat([num_features, route_type_ohe, features_ohe,
                              activities_ohe])
    logger.info("User input successfully converted to featurized vector")

    return input_vector


def scaled_cosine_sim(df):
    """Calculate the cosine similarity  of a dataframe.

        Args:
            df (:obj:`pandas.DataFrame`): data to calculate distance

        Returns:
            cs (`numpy.array`): Distance matrix using cosine similarity

    """

    # Standard scaling for numerical data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Calculate distance
    cs = cosine_similarity(df_scaled)
    logger.info("Cosine similarity matrix created")

    return cs


def recommend_trails(n, df_features, trail_id, response, input_vector):
    """Recommend n most similar trails to user input

        Args:
            n (int): number of similar trails to return
            df_features (:obj:`pandas.DataFrame`): dataframe of features
            trail_id (str): name of trail_id column
            response (str): name of response column
            input_vector (`pandas.Series`): series of user inputs

        Returns:
            most_sim_id (:obj:`list` of `int`): list of trail ids

    """

    # Set trail_id to be the index
    input_matrix = df_features.set_index(trail_id)
    input_matrix = input_matrix.drop(columns=[response])

    # Save trail ids to reference for recommendation
    input_matrix_ind = input_matrix.index

    # Insert new input in first row, use this to calculate similarity
    input_dist = pd.concat([pd.DataFrame(input_vector).transpose(),
                            input_matrix])

    # Calculate distance
    cs = scaled_cosine_sim(input_dist)
    logger.debug("Cosine similarity calculated against user input")

    # Get similarities for the new input
    sim_vec = cs[0, :]

    # Get the n largest similarities
    sim_ind = sim_vec.argsort()[-(n + 1):][::-1][1:]

    # Get the trail id using the index
    most_sim_id = list(input_matrix_ind[sim_ind])
    logger.info("%s most similar trail ids found", n)

    return most_sim_id


def predict_difficulty(input_vector, model_path):
    """Predict the difficulty of a trail

        Args:
            input_vector (`pandas.Series`): series of user inputs
            model_path (str): path to model

        Returns:
            most_sim_id (:obj:`list` of `int`): list of trail ids

    """
    # Make prediction
    input_arr = np.array(input_vector).reshape(1, -1)
    try:
        model = pickle.load(open(model_path, 'rb'))
    except FileNotFoundError as e:
        logger.error("Model file not found. Please make sure path is correct.")

    pred = model.predict(input_arr)[0]
    logger.info("Model made prediction on user input")

    return pred


def predict(length_input, elevation_gain_input, route_type_input,
            features_input, activities_input,
            features_name, full_features_ls_path, activities_name,
            full_activities_ls_path, clean_data_path, route_type,
            model_path):
    """Make a prediction on trail difficulty based on user inputs."""

    try:
        df = pd.read_csv(clean_data_path)
    except FileNotFoundError as e:
        logger.error("Clean data not found. Please make sure file path is"
                     "correct.")

    try:
        with open(full_features_ls_path) as f:
            full_features_ls = [line.rstrip() for line in f]
    except FileNotFoundError as e:
        logger.error("Features list file not found")

    try:
        with open(full_activities_ls_path) as f:
            full_activities_ls = [line.rstrip() for line in f]
    except FileNotFoundError as e:
        logger.error("Activities list file not found")

    dict_input = collect_input(length_input, elevation_gain_input,
                               route_type_input, features_input,
                               activities_input)
    user_input = create_input_features(features_name, full_features_ls,
                                       activities_name, full_activities_ls,
                                       df, route_type,
                                       dict_input)

    return predict_difficulty(user_input, model_path)


def recommend(length_input, elevation_gain_input, route_type_input,
              features_input, activities_input,
              features_name, full_features_ls_path, activities_name,
              full_activities_ls_path, clean_data_path,
              route_type, n, featurize_path, trail_id, response):
    """Provide top n recommendations on most similar trails."""

    try:
        df = pd.read_csv(clean_data_path)
    except FileNotFoundError as e:
        logger.error("Clean data file not found. Please make sure path is"
                     "correct")

    try:
        df_features = pd.read_csv(featurize_path)
    except FileNotFoundError as e:
        logger.error("Featurized data not found. Please make sure path is"
                     "correct")

    with open(full_features_ls_path) as f:
        full_features_ls = [line.rstrip() for line in f]

    with open(full_activities_ls_path) as f:
        full_activities_ls = [line.rstrip() for line in f]

    dict_input = collect_input(length_input, elevation_gain_input,
                               route_type_input, features_input,
                               activities_input)
    user_input = create_input_features(features_name, full_features_ls,
                                       activities_name, full_activities_ls,
                                       df, route_type,
                                       dict_input)

    return recommend_trails(n, df_features, trail_id, response, user_input)

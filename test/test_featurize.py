import pandas as pd
import pytest

from src.featurize import one_hot_encode


def test_one_hot_encode():
    # Define input dataframe
    df_in_values = [[10037153, 'Waterton Valley Trail', 'Glacier National Park',
                     'Babb', 'Montana', 'United States',
                     "{'lat': 48.95776, 'lng': -113.89222}", 3.5294, 18.47,
                     1148.7912,
                     7, 'out and back', 2.0, 4.5, 3,
                     "['dogs-no', 'forest', 'lake', 'river', 'wild-flowers', "
                     "'wildlife']",
                     "['backpacking', 'camping', 'hiking', 'nature-trips']",
                     'i'],
                    [10265905, 'South Kaibab Trail to Ooh Aah Point',
                     'Grand Canyon National Park', 'Grand Canyon', 'Arizona',
                     'United States', "{'lat': 36.05309, 'lng': -112.08387}",
                     28.8685,
                     1.65, 210.9216, 3, 'out and back', 3.0, 5.0, 455,
                     "['dogs-no', 'views', 'wildlife']",
                     "['birding', 'hiking', 'nature-trips', 'walking']", 'i'],
                    [10038226, 'Apgar Lookout Trail', 'Glacier National Park',
                     'Columbia Falls', 'Montana', 'United States',
                     "{'lat': 48.50434, 'lng': -114.02082}", 15.4183, 6.49,
                     566.928,
                     5, 'out and back', 3.0, 4.0, 220,
                     "['dogs-no', 'forest', 'river', 'views', 'wild-flowers', "
                     "'wildlife']",
                     "['birding', 'hiking', 'nature-trips']", 'i']]

    df_in_index = [1572, 33, 1475]

    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    df_true = pd.DataFrame(
        [[10037153, 18.47, 1148.7912,
          "['dogs-no', 'forest', 'lake', 'river', 'wild-flowers', 'wildlife']",
          "['backpacking', 'camping', 'hiking', 'nature-trips']", 7],
         [10265905, 1.65, 210.9216, "['dogs-no', 'views', 'wildlife']",
          "['birding', 'hiking', 'nature-trips', 'walking']", 3],
         [10038226, 6.49, 566.928,
          "['dogs-no', 'forest', 'river', 'views', 'wild-flowers', 'wildlife']",
          "['birding', 'hiking', 'nature-trips']", 5]],
        index=[1572, 33, 1475],
        columns=['trail_id', 'length', 'elevation_gain', 'features',
                 'activities',
                 'difficulty_rating'])

    # Create test output
    df_test = one_hot_encode(df_in, 'trail_id', ['features', 'activities'],
                             ['length', 'elevation_gain', 'route_type'],
                             'difficulty_rating')

    assert df_test.equals(df_true)


def test_one_hot_encode_key_error():
    # Define input dataframe
    df_in_values = [[10037153, 'Waterton Valley Trail', 'Glacier National Park',
                     'Babb', 'Montana', 'United States',
                     "{'lat': 48.95776, 'lng': -113.89222}", 3.5294, 18.47,
                     1148.7912,
                     7, 'out and back', 2.0, 4.5, 3,
                     "['dogs-no', 'forest', 'lake', 'river', 'wild-flowers', "
                     "'wildlife']",
                     "['backpacking', 'camping', 'hiking', 'nature-trips']",
                     'i'],
                    [10265905, 'South Kaibab Trail to Ooh Aah Point',
                     'Grand Canyon National Park', 'Grand Canyon', 'Arizona',
                     'United States', "{'lat': 36.05309, 'lng': -112.08387}",
                     28.8685,
                     1.65, 210.9216, 3, 'out and back', 3.0, 5.0, 455,
                     "['dogs-no', 'views', 'wildlife']",
                     "['birding', 'hiking', 'nature-trips', 'walking']", 'i'],
                    [10038226, 'Apgar Lookout Trail', 'Glacier National Park',
                     'Columbia Falls', 'Montana', 'United States',
                     "{'lat': 48.50434, 'lng': -114.02082}", 15.4183, 6.49,
                     566.928,
                     5, 'out and back', 3.0, 4.0, 220,
                     "['dogs-no', 'forest', 'river', 'views', 'wild-flowers', "
                     "'wildlife']",
                     "['birding', 'hiking', 'nature-trips']", 'i']]
    df_in_index = [1572, 33, 1475]
    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    with pytest.raises(KeyError):
        one_hot_encode(df_in, 'trail_id', ['features', 'activities'],
                       ['length', 'elevation_gain', 'route_type'], 'error')


def test_one_hot_encode_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(TypeError):
        one_hot_encode(df_in, 'trail_id', ['features', 'activities'],
                       ['length', 'elevation_gain', 'route_type'],
                       'difficulty_rating')

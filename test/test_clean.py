import pandas as pd
import pytest

from src.clean import df_drop_str
from src.clean import yards_to_miles


def test_yards_to_miles():
    # Define input dataframe
    df_in_values = [[10008848, 'Baxter Creek Trail',
                     'Great Smoky Mountains National Park', 'Waynesville',
                     'North Carolina', 'United States',
                     "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 25266.638,
                     1522.7808, 5, 'point to point', 2.0, 4.5, 7,
                     "['dogs-no', 'forest', 'views', 'wild-flowers']",
                     "['birding', 'hiking', 'nature-trips']", 'i'],
                    [10032315, 'Sunnybrook Meadows Trail',
                     'Olympic National Park',
                     'Brinnon', 'Washington', 'United States',
                     "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 26393.176,
                     2102.8152, 7, 'out and back', 2.0, 5.0, 1,
                     "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips']",
                     'i'],
                    [10027503, 'Clouds Rest Trail via Tenaya Lake',
                     'Yosemite National Park', 'Yosemite Valley', 'California',
                     'United States', "{'lat': 37.82585, 'lng': -119.47046}",
                     38.5795,
                     19794.882, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
                     "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers',"
                     " 'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking',"
                     " 'nature-trips', 'trail-running', 'horseback-riding']",
                     'i']]
    df_in_index = [1698, 2919, 224]
    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    df_true = pd.DataFrame(
        [[10008848, 'Baxter Creek Trail',
          'Great Smoky Mountains National Park', 'Waynesville',
          'North Carolina', 'United States',
          "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 14.36, 1522.7808,
          5, 'point to point', 2.0, 4.5, 7,
          "['dogs-no', 'forest', 'views', 'wild-flowers']",
          "['birding', 'hiking', 'nature-trips']", 'i'],
         [10032315, 'Sunnybrook Meadows Trail', 'Olympic National Park',
          'Brinnon', 'Washington', 'United States',
          "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 15.0, 2102.8152,
          7, 'out and back', 2.0, 5.0, 1,
          "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
          "['backpacking', 'birding', 'camping', 'hiking', 'nature-trips']",
          'i'],
         [10027503, 'Clouds Rest Trail via Tenaya Lake',
          'Yosemite National Park', 'Yosemite Valley', 'California',
          'United States', "{'lat': 37.82585, 'lng': -119.47046}", 38.5795,
          11.25, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
          "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers', 'wildlife']",
          "['backpacking', 'birding', 'camping', 'hiking', 'nature-trips', "
          "'trail-running', 'horseback-riding']",
          'i']],
        index=[1698, 2919, 224],
        columns=['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                 'country_name', '_geoloc', 'popularity', 'length',
                 'elevation_gain',
                 'difficulty_rating', 'route_type', 'visitor_usage',
                 'avg_rating',
                 'num_reviews', 'features', 'activities', 'units'])

    # Create test output
    df_test = yards_to_miles(df_in, 'length', 2)

    assert df_test.equals(df_true)


def test_yards_to_miles_key_error():
    # Define input dataframe
    df_in_values = [[10008848, 'Baxter Creek Trail',
                     'Great Smoky Mountains National Park', 'Waynesville',
                     'North Carolina', 'United States',
                     "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 25266.638,
                     1522.7808, 5, 'point to point', 2.0, 4.5, 7,
                     "['dogs-no', 'forest', 'views', 'wild-flowers']",
                     "['birding', 'hiking', 'nature-trips']", 'i'],
                    [10032315, 'Sunnybrook Meadows Trail',
                     'Olympic National Park',
                     'Brinnon', 'Washington', 'United States',
                     "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 26393.176,
                     2102.8152, 7, 'out and back', 2.0, 5.0, 1,
                     "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips']",
                     'i'],
                    [10027503, 'Clouds Rest Trail via Tenaya Lake',
                     'Yosemite National Park', 'Yosemite Valley', 'California',
                     'United States', "{'lat': 37.82585, 'lng': -119.47046}",
                     38.5795,
                     19794.882, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
                     "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers', "
                     "'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips', 'trail-running', 'horseback-riding']",
                     'i']]
    df_in_index = [1698, 2919, 224]
    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    with pytest.raises(KeyError):
        yards_to_miles(df_in, 'error', 2)


def test_yards_to_miles_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(TypeError):
        yards_to_miles(df_in, 'length', 2)


def test_df_drop_str():
    # Define input dataframe
    df_in_values = [[10008848, 'Baxter Creek Trail',
                     'Great Smoky Mountains National Park', 'Waynesville',
                     'North Carolina', 'United States',
                     "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 25266.638,
                     1522.7808, 5, 'point to point', 2.0, 4.5, 7,
                     "['dogs-no', 'forest', 'views', 'wild-flowers']",
                     "['birding', 'hiking', 'nature-trips']", 'i'],
                    [10032315, 'Sunnybrook Meadows Trail',
                     'Olympic National Park',
                     'Brinnon', 'Washington', 'United States',
                     "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 26393.176,
                     2102.8152, 7, 'out and back', 2.0, 5.0, 1,
                     "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips']",
                     'i'],
                    [10027503, 'Clouds Rest Trail via Tenaya Lake',
                     'Yosemite National Park', 'Yosemite Valley', 'California',
                     'United States', "{'lat': 37.82585, 'lng': -119.47046}",
                     38.5795,
                     19794.882, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
                     "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers', "
                     "'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips', 'trail-running', 'horseback-riding']",
                     'i']]
    df_in_index = [1698, 2919, 224]
    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    df_true = pd.DataFrame(
        [[10008848, 'Baxter Creek Trail',
          'Great Smoky Mountains National Park', 'Waynesville',
          'North Carolina', 'United States',
          "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 25266.638,
          1522.7808, 5, 'point to point', 2.0, 4.5, 7,
          "['dogs-no', 'forest', 'views', 'wild-flowers']",
          "['birding', 'hiking', 'nature-trips']", 'i'],
         [10032315, 'Sunnybrook Meadows Trail', 'Olympic National Park',
          'Brinnon', 'Washington', 'United States',
          "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 26393.176,
          2102.8152, 7, 'out and back', 2.0, 5.0, 1,
          "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
          "['backpacking', 'birding', 'camping', 'hiking', 'nature-trips']",
          'i'],
         [10027503, 'Clouds Rest Trail via Tenaya Lake',
          'Yosemite National Park', 'Yosemite Valley', 'California',
          'United States', "{'lat': 37.82585, 'lng': -119.47046}", 38.5795,
          19794.882, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
          "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers', 'wildlife']",
          "['backpacking', 'birding', 'camping', 'hiking', 'nature-trips', "
          "'trail-running', 'horseback-riding']",
          'i']],
        index=[1698, 2919, 224],
        columns=['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                 'country_name', '_geoloc', 'popularity', 'length',
                 'elevation_gain',
                 'difficulty_rating', 'route_type', 'visitor_usage',
                 'avg_rating',
                 'num_reviews', 'features', 'activities', 'units'])

    # Create test output
    df_test = df_drop_str(df_in, 'name', 'closed')

    assert df_test.equals(df_true)


def test_df_drop_str_key_error():
    # Define input dataframe
    df_in_values = [[10008848, 'Baxter Creek Trail',
                     'Great Smoky Mountains National Park', 'Waynesville',
                     'North Carolina', 'United States',
                     "{'lat': 35.75111, 'lng': -83.10966}", 4.9204, 25266.638,
                     1522.7808, 5, 'point to point', 2.0, 4.5, 7,
                     "['dogs-no', 'forest', 'views', 'wild-flowers']",
                     "['birding', 'hiking', 'nature-trips']", 'i'],
                    [10032315, 'Sunnybrook Meadows Trail',
                     'Olympic National Park',
                     'Brinnon', 'Washington', 'United States',
                     "{'lat': 47.72974, 'lng': -123.14179}", 3.0804, 26393.176,
                     2102.8152, 7, 'out and back', 2.0, 5.0, 1,
                     "['dogs-no', 'views', 'wild-flowers', 'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking',"
                     " 'nature-trips']",
                     'i'],
                    [10027503, 'Clouds Rest Trail via Tenaya Lake',
                     'Yosemite National Park', 'Yosemite Valley', 'California',
                     'United States', "{'lat': 37.82585, 'lng': -119.47046}",
                     38.5795,
                     19794.882, 948.8424, 5, 'out and back', 3.0, 5.0, 685,
                     "['dogs-no', 'forest', 'lake', 'views', 'wild-flowers', "
                     "'wildlife']",
                     "['backpacking', 'birding', 'camping', 'hiking', "
                     "'nature-trips', 'trail-running', 'horseback-riding']",
                     'i']]
    df_in_index = [1698, 2919, 224]
    df_in_columns = ['trail_id', 'name', 'area_name', 'city_name', 'state_name',
                     'country_name', '_geoloc', 'popularity', 'length',
                     'elevation_gain',
                     'difficulty_rating', 'route_type', 'visitor_usage',
                     'avg_rating',
                     'num_reviews', 'features', 'activities', 'units']
    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output
    with pytest.raises(KeyError):
        df_drop_str(df_in, 'error', 'closed')


def test_df_drop_str_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(TypeError):
        df_drop_str(df_in, 'name', 'closed')

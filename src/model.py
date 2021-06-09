import logging.config
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def train(df, trail_id, response, test_size, random_state_split,
          random_state_model, model_path, x_test_path, y_test_path):
    """Train a random forest classifier.

            Args:
                df (:obj:`pandas.DataFrame`): path to features dataframe
                trail_id (str): name of trail id column
                response (str): name of response variable
                test_size (float): proportion of the data to be included in the
                tests set
                random_state_split (float): random state for the train, tests,
                split function
                random_state_model (float): random state for the model
                model_path (str): path to save the model
                x_test_path (str): path to save x test
                y_test_path (str): path to save y test

            Returns:
                None
    """
    # Subset features and response
    try:
        X = df.drop(columns=[response, trail_id], axis=1)
        y = df[response]
    except KeyError as e:
        logger.error("Please make sure columns are in the dataframe")

    # Train, test, split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=
                                                        test_size, random_state=
                                                        random_state_split)
    logger.info("Data successfully split into train and test")

    # Train the model
    clf = RandomForestClassifier(random_state=random_state_model,
                                 n_estimators=10)
    clf = clf.fit(X_train, y_train)
    logger.debug("Random forest classifier trained and fit on data")

    # Save the model
    pickle.dump(clf, open(model_path, 'wb'))
    logger.info("Model saved to %s", model_path)

    # Save the test features and labels
    np.savetxt(x_test_path, X_test, delimiter=",", fmt='%s')
    np.savetxt(y_test_path, y_test, delimiter=",", fmt='%s')


def evaluate(cv, model_path, x_test_path, y_test_path, scoring, cm_labels,
             output_path):
    """Evaluate a random forest classifier.

        Args:
            cv (int): number of folds in cross validation
            model_path (str): path to model path
            x_test_path (str): path to x test
            y_test_path (str): path to y test
            scoring (str): type of scoring
            cm_labels (:obj:`list` of :obj:`str`): labels of confusion matrix
            output_path (str): path to save evaluation metrics

        Returns:
            None

    """
    # Load model, x_test, and y_test
    try:
        clf = pickle.load(open(model_path, 'rb'))
        X_test = pd.read_csv(x_test_path, sep=',')
        y_test = pd.read_csv(y_test_path, sep=',').values.ravel()
    except FileNotFoundError as e:
        logger.error("Please make sure file paths are correct")

    # Get predictions
    ypred_bin_test = clf.predict(X_test)
    logger.debug("Model successfully predicted on test")

    # Calculate evaluation metrics
    cv_score = cross_val_score(clf, X_test, y_test, cv=cv, scoring=scoring)
    logger.debug("Cross validated score calculated")
    logger.info("Mean cross validation score is %s", np.mean(cv_score))
    logger.info("Variance cross validation score is %s", np.var(cv_score))
    confusion = confusion_matrix(y_test, ypred_bin_test, labels=cm_labels)
    logger.debug("Confusion matrix created")

    # Save results to a text file
    f = open(output_path, "w+")
    f.write('Mean CV score: {:.3f}'.format(cv_score.mean()))
    f.write('Var CV score  {:.3f}'.format(cv_score.std()))
    f.write('\n')
    f.write(pd.DataFrame(confusion,
                         index=cm_labels,
                         columns=cm_labels).to_string())
    f.close()
    logger.info("Evaluation metrics successfully saved to %s", output_path)


def model(featurize_path, trail_id, response,
          test_size, random_state_split, random_state_model,
          model_path, x_test_path, y_test_path,
          cv, scoring, cm_labels, output_path):
    """Build a random forest model and evaluate the model."""

    # Read featurize data
    try:
        df = pd.read_csv(featurize_path)
    except FileNotFoundError as e:
        logger.error("File could not be found. Please make sure file path is"
                     "correct.")

    # Train random forest
    train(df, trail_id, response, test_size, random_state_split,
          random_state_model, model_path, x_test_path,
          y_test_path)
    logger.info('Model training finished')

    # Evaluate random forest
    evaluate(cv, model_path, x_test_path, y_test_path, scoring, cm_labels,
             output_path)
    logger.info('Model evaluation results saved to %s', output_path)

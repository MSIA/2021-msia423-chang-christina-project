import logging.config

import numpy as np
import pandas as pd
import pickle

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)


def train(df, trail_id, response, test_size, random_state_split, random_state_model,
          model_path, x_test_path, y_test_path):

    # Train, test, split
    X = df.drop(columns=[response, trail_id], axis=1)
    y = df[response]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state_split)

    # Train the model
    clf = RandomForestClassifier(random_state=random_state_model, n_estimators=10)
    clf = clf.fit(X_train, y_train)

    # Save the model
    pickle.dump(clf, open(model_path, 'wb'))

    # Save the test features and labels
    np.savetxt(x_test_path, X_test, delimiter=",", fmt='%s')
    np.savetxt(y_test_path, y_test, delimiter=",", fmt='%s')


def evaluate(cv, model_path, x_test_path, y_test_path, scoring, cm_labels, output_path):
    # Load model, x_test, and y_test
    clf = pickle.load(open(model_path, 'rb'))
    X_test = pd.read_csv(x_test_path, sep=',')
    y_test = pd.read_csv(y_test_path, sep=',').values.ravel()

    # Get predictions and probabilities
    ypred_proba_test = clf.predict_proba(X_test)[:, 1]
    ypred_bin_test = clf.predict(X_test)

    # Calculate evaluation metrics
    cv_score = cross_val_score(clf, X_test, y_test, cv=cv, scoring=scoring)
    confusion = confusion_matrix(y_test, ypred_bin_test, labels=cm_labels)

    print('Mean CV score: {:.3f}'.format(cv_score.mean()))
    print('Var CV score  {:.3f}'.format(cv_score.std()))
    print()
    print(pd.DataFrame(confusion,
                       index=cm_labels,
                       columns=cm_labels))

    # Save results to a text file
    f = open(output_path, "w+")
    f.write('Mean CV score: {:.3f}'.format(cv_score.mean()))
    f.write('Var CV score  {:.3f}'.format(cv_score.std()))
    f.write('\n')
    f.write(pd.DataFrame(confusion,
                         index=cm_labels,
                         columns=cm_labels).to_string())
    f.close()


def model(featurize_path, trail_id, response,
          test_size, random_state_split, random_state_model,
          model_path, x_test_path, y_test_path,
          cv, scoring, cm_labels, output_path):

    # Read featurize data
    df = pd.read_csv(featurize_path)

    # Train random forest
    train(df, trail_id, response, test_size, random_state_split, random_state_model, model_path, x_test_path,
          y_test_path)
    logger.info('Model training finished.')

    # Evaluate random forest
    evaluate(cv, model_path, x_test_path, y_test_path, scoring, cm_labels, output_path)
    logger.info('Model evaluation results saved.')

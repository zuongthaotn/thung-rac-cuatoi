from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import AI.constants as ai_constants
from sklearn.ensemble import IsolationForest

if __name__ == "__main__":
    csv_file = '{0}/VN30ps/data/VN30F1M_for_gradient_boosting2.csv'.format(str(ai_constants.AI_DIR))
    df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
    df.dropna(inplace=True)
    # df = df[df['MA5_MA20_rate'] < 2]
    # df = df[df['MA5_MA20'] < 0.7]

    # split dataset in features and target variable
    feature_cols = ["short_trend", "Today_Up_Down", "Volatility_ATR", "Body_Candlestick_Rate", "Tail_Candlestick_Rate",
                    "Yesterday_Up_Down", "MA5_MA20", "MA5_MA20_rate", "RSI_10_Simple", "Next_Open_Is_Lower"]
    X = df[feature_cols]  # Features
    y = df.Next_Low_Is_Lower  # Target variable

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42)  # 70% training and 30% test

    iso = IsolationForest(contamination=0.1)
    goodTrain = iso.fit_predict(X_train)
    # select all rows that are not outliers
    mask = goodTrain != -1
    X_train, y_train = X_train[mask], y_train[mask]

    goodTest = iso.fit_predict(X_test)
    mask_ = goodTest != -1
    X_test, y_test = X_test[mask_], y_test[mask_]



    # from sklearn.model_selection import GridSearchCV
    # LR = {'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1], 'random_state': [50, 100, 150, 200],
    #       'n_estimators': [50, 100, 150, 200]}
    # tuning = GridSearchCV(estimator=GradientBoostingClassifier(), param_grid=LR, scoring="accuracy")
    # tuning.fit(X_train, y_train)
    # print(tuning.best_params_)
    # print(tuning.best_score_)
    # exit()

    # Create GradientBoostingClassifier model
    gbc = GradientBoostingClassifier(learning_rate=0.01, random_state=50, n_estimators=150)

    # Train
    gbc = gbc.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = gbc.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("R2_score:", metrics.r2_score(y_test, y_pred))

    import pickle
    import os
    from pathlib import Path

    current_folder = Path(__file__).parent
    trainner_file = str(current_folder) + '/GradientBoostingClassifier_next_low.pickle'
    if not os.path.isfile(trainner_file):
        with open(trainner_file, 'wb') as fp:
            pickle.dump(gbc, fp)

    # pred_label = gbc.predict(X)
    # algo_result = df.assign(Predicts=pred_label)

    # algo_result.to_csv(str(current_folder) + '/algo_result.csv')

    # algo_wrong_result = algo_result.loc[(algo_result.Next_Low_Is_Lower != algo_result.Predicts)]
    # algo_wrong_result.to_csv(str(current_folder) + '/algo_wrong_result.csv')
    # exit()
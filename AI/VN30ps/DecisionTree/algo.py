from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd

if __name__ == "__main__":
    from pathlib import Path
    current_folder = Path(__file__).parent
    weather_file = str(current_folder) + '/VN30F1M_for_decision_tree.csv'
    df = pd.read_csv(weather_file, index_col=0, parse_dates=True)
    df.dropna(inplace=True)

    # split dataset in features and target variable
    feature_cols = ["short_trend", "long_trend", "Today_Up_Down", "Candlestick_Rate", "MA5_above_MA20", "RSI_10_Simple"]
    X = df[feature_cols]  # Features
    y = df.Next_Low_Is_Lower  # Target variable

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=1)  # 70% training and 30% test

    # Create Decision Tree classifier object
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=6, max_leaf_nodes=50)

    # Train Decision Tree Classifier
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # from sklearn import tree
    # import matplotlib.pyplot as plt
    #
    # fig = plt.figure(figsize=(50, 40))
    # _ = tree.plot_tree(clf,
    #                    feature_names=feature_cols,
    #                    class_names=["Down", "Up"],
    #                    filled=True)
    #
    # VN30F1M_tree = str(current_folder) + '/VN30F1M_decision_tree.png'
    # fig.savefig(VN30F1M_tree)

    pred_label = clf.predict(X)
    xxx = df.assign(Predicts=pred_label)
    from pathlib import Path

    current_folder = Path(__file__).parent
    xxx.to_csv(str(current_folder) + '/algo_result.csv')
    exit()
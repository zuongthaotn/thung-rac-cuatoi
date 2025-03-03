from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import AI.constants as ai_constants

if __name__ == "__main__":
    csv_file = '{0}/VN30ps/data/VN30F1M_for_gradient_boosting.csv'.format(str(ai_constants.AI_DIR))
    df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
    df.dropna(inplace=True)

    # split dataset in features and target variable
    feature_cols = ["short_trend", "long_trend", "Today_Up_Down", "Candlestick_Rate", "MA5_above_MA20", "RSI_10_Simple",
                    "Next_Open_Is_Lower"]
    X = df[feature_cols]  # Features
    y = df.Next_Low_Is_Lower  # Target variable

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=1)  # 70% training and 30% test

    kmeans = KMeans(n_clusters=2, n_init=2).fit(X_train)

    # Predict the response for test dataset
    y_pred = kmeans.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
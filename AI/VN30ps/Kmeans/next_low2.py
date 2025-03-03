from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    current_folder = Path(__file__).parent
    vn30f1m_file = str(current_folder) + '/VN30F1M_KMeans.csv'
    df = pd.read_csv(vn30f1m_file, index_col=0, parse_dates=True)
    df.dropna(inplace=True)

    # split dataset in features and target variable
    feature_cols = ["RSI_trend", "EMA_H", "pass_1_return", "today_return"]
    X = df[feature_cols]  # Features
    y = df.Next_Low_Is_Lower  # Target variable

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=42)  # 70% training and 30% test

    kmeans = KMeans(n_clusters=2, n_init=2).fit(X_train)

    # Predict the response for test dataset
    y_pred = kmeans.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
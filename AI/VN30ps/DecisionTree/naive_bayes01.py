#Import scikit-learn dataset library
from sklearn import datasets
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

if __name__ == "__main__":
    from pathlib import Path
    current_folder = Path(__file__).parent
    weather_file = str(current_folder) + '/VN30F1M_for_decision_tree.csv'
    df = pd.read_csv(weather_file, index_col=0, parse_dates=True)

    # split dataset in features and target variable
    feature_cols = ["short_trend", "long_trend", "Today_Up_Down", "Candlestick_Rate", "MA5_above_MA20", "RSI_10_Simple"]
    X = df[feature_cols]  # Features
    y = df.Next_Low_Is_Lower  # Target variable

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=1)  # 70% training and 30% test

    # Instantiate: create object
    gnb = GaussianNB()

    # Train the model using the training sets 	y_pred=clf.predict(X_test)
    gnb.fit(X_train, y_train)

    y_pred = gnb.predict(X_test)
    # Sau khi đào tạo, kiểm tra tính chính xác bằng cách sử dụng giá trị thực tế và dự đoán.
    # Import scikit-learn metrics module for accuracy calculation
    from sklearn import metrics

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

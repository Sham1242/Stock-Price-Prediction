import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder

def gnb_predict(stock_name):
    # Load and preprocess data
    data = yf.download(stock_name, period="1mo", interval="1d")
    data = data.dropna()

    # Create features and target variables
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    y = data['Adj Close'].shift(-1)  # Use adjusted close price as the target variable

    # Drop the last row since it will have a NaN value for y
    X = X[:-1]
    y = y[:-1]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train the Gaussian Naive Bayes model
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    # Predict the target variable for the test set
    y_pred = gnb.predict(X_test)

    # Create a LabelEncoder object
    label_encoder = LabelEncoder()

    # Convert predicted labels back to original format
    y_pred = label_encoder.inverse_transform(y_pred)

    return y_pred

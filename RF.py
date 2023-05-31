import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def random_forest_predict(stock_name):
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, shuffle=False)

    # Train the Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Predict the target variable for the test set
    y_pred = rf.predict(X_test)

    # Calculate mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    return y_pred

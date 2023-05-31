import yfinance as yf
from sklearn.neighbors import KNeighborsRegressor

def generate_predicted_data(stock_symbol):
    data = yf.download(stock_symbol, period="2mo", interval="1d")

    # Preprocess the data
    data = data.dropna()
    X = data[['Open', 'High', 'Low']].values
    y = data['Close'].values

    train_size = int(len(data) * 0.8)  # 80% for training
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    return y_pred
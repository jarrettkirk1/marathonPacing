from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

# Example usage
if __name__ == "__main__":
    from data_preprocessing import load_data, preprocess_pacing_data, fill_missing_values, scale_data, prepare_train_test_split

    data = load_data('boston_marathon_min_km_pivoted.csv')
    data = preprocess_pacing_data(data)
    data = fill_missing_values(data)
    data_scaled_df = scale_data(data)
    X_train, X_test, y_train, y_test = prepare_train_test_split(data_scaled_df, 'Finish Net')

    model = train_model(X_train, y_train)
    mse, r2 = evaluate_model(model, X_test, y_test)
    print(f'Mean Squared Error: {mse}, R2 Score: {r2}')

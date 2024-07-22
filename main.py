from data_preprocessing import load_data, preprocess_pacing_data, fill_missing_values, scale_data, prepare_train_test_split
from model_training import train_model, evaluate_model

def main():
    data = load_data('boston_marathon_min_km_pivoted.csv')
    data = preprocess_pacing_data(data)
    data = fill_missing_values(data)
    data_scaled_df = scale_data(data)
    X_train, X_test, y_train, y_test = prepare_train_test_split(data_scaled_df, 'Finish Net')

    model = train_model(X_train, y_train)
    mse, r2 = evaluate_model(model, X_test, y_test)
    print(f'Mean Squared Error: {mse}, R2 Score: {r2}')

if __name__ == "__main__":
    main()

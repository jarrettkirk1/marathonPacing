import pandas as pd
from scripts.data_preprocessing import load_data, preprocess_pacing_data, fill_missing_values, scale_data, prepare_train_test_split
from scripts.model_training import train_model, evaluate_model

def main():
    # Load data
    data = load_data('boston_marathon_min_km_pivoted.csv')
    
    # Preprocess data
    data = preprocess_pacing_data(data)
    data = fill_missing_values(data)
    data_scaled_df = scale_data(data)
    
    # Split data
    X_train, X_test, y_train, y_test = prepare_train_test_split(data_scaled_df, 'Finish Net')
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()

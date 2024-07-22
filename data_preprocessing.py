import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def convert_pace_to_numeric(pace_str):
    if pd.isnull(pace_str) or pace_str == '-':
        return np.nan
    parts = str(pace_str).split(':')
    return int(parts[0]) + int(parts[1]) / 60

def preprocess_pacing_data(data):
    for col in data.columns[1:]:
        data[col] = data[col].apply(convert_pace_to_numeric)
    return data

def load_elevation_data(elevation_path, distance_path):
    elevation_data = np.load(elevation_path)
    distance_data = np.load(distance_path)
    elevation_df = pd.DataFrame({
        'Distance': distance_data,
        'Elevation': elevation_data
    })
    return elevation_df

def fill_missing_values(data):
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())
    return data

def scale_data(data):
    scaler = StandardScaler()
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data_scaled = scaler.fit_transform(data[numeric_cols])
    data_scaled_df = pd.DataFrame(data_scaled, columns=numeric_cols)
    data_scaled_df['Athlete Name'] = data['Athlete Name']
    return data_scaled_df

def prepare_train_test_split(data_scaled_df, target_col, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    X = data_scaled_df.drop(columns=[target_col, 'Athlete Name'])
    y = data_scaled_df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

# Example usage
if __name__ == "__main__":
    data = load_data('boston_marathon_min_km_pivoted.csv')
    data = preprocess_pacing_data(data)
    data = fill_missing_values(data)
    data_scaled_df = scale_data(data)
    X_train, X_test, y_train, y_test = prepare_train_test_split(data_scaled_df, 'Finish Net')
    print(X_train.shape, X_test.shape)

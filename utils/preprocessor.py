import pandas as pd
import os

def load_and_combine_data():
    base_path = os.path.dirname(__file__)
    data_path = os.path.abspath(os.path.join(base_path, "..", "data"))

    normal_path = os.path.join(data_path, "normal_data.csv")
    malicious_path = os.path.join(data_path, "malicious_data.csv")

    # Load both datasets
    normal_df = pd.read_csv(normal_path)
    malicious_df = pd.read_csv(malicious_path)

    # Combine and shuffle
    combined_df = pd.concat([normal_df, malicious_df], ignore_index=True)
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)

    return combined_df

import pandas as pd  

def clean_threat_data(path):
    df = pd.read_csv(path)
    df.dropna(inplace=True)
    df["threat_numeric"] = df["threat_level"].str.extract(r'(\d)').astype(int)
    return df
    
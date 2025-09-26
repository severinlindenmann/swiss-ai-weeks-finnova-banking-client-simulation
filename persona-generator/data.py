import pandas as pd
from pathlib import Path

def load_demographie_csv():
  csv_path = Path(__file__).parent / "../data/Demographie/datax.csv"
  df = pd.read_csv(csv_path, low_memory=False)
  return df

def filter_df_by_params(df, params):
  for key, value in params.items():
    if value is not None:
      df = df[df[key] == value]
  return df


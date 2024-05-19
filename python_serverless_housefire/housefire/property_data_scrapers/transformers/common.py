import pandas as pd


def df_to_request(df: pd.DataFrame, ticker: str):
    """
    Convert a pandas DataFrame to a list of dictionaries
    """
    df_with_reit = df.assign(reit=ticker)
    return df_with_reit.to_dict(orient="records")

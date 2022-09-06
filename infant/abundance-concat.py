import pandas as pd


if __name__ == '__main__':
    df_1 = pd.read_csv('abundance-1.csv')
    df_2 = pd.read_csv('abundance-2.csv')
    
    df_merged = pd.merge(df_1, df_2, how="outer").fillna(0)
    df_merged.to_csv('abundance.csv', index=0)
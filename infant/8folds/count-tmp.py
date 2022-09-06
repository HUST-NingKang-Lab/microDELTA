import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('meta_withbirth.csv')
    df_count = df.groupby('Env').count()
    df_count.columns = ['counts']
    print(df_count)
    print(df_count['counts'].sum())
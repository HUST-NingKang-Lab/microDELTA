import pandas as pd
from sklearn.model_selection import KFold


if __name__ == '__main__':
    metadata = pd.read_csv('meta_withbirth.csv')
    abundance = pd.read_csv('abundance.csv')
    
    kf =KFold(n_splits=8)
    i = 1
    for train_index,test_index in kf.split(metadata['SampleID']):
        metadata.loc[list(train_index)].to_csv(f'./group{i}/train-meta.csv', index=0)
        metadata.loc[list(test_index)].to_csv(f'./group{i}/test-meta.csv', index=0)
        df_train = abundance[metadata.loc[list(train_index)]['SampleID']]
        df_train.insert(0, 'Samples', abundance['Samples'])
        df_train.to_csv(f'./group{i}/train-abundance.tsv', sep='\t', index=0)
        df_test = abundance[metadata.loc[list(test_index)]['SampleID']]
        df_test.insert(0, 'Samples', abundance['Samples'])
        df_test.to_csv(f'./group{i}/test-abundance.tsv', sep='\t', index=0)
        i = i+1
        
        
        
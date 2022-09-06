import pandas as pd
    
if __name__ == '__main__':
    meta1 = pd.read_csv('metadata.csv')
    meta2 = pd.read_csv('experiment_paired_fastq_spreadsheet_template_Baby.tsv', sep='\t')
    meta_withbirth = meta1
    age_withbirth = []
    
    for i in meta2.index:
        if meta2.loc[i, 'mode_of_birth'] == 'sectio':
            age_withbirth.append(f"{meta1.loc[i, 'Env']}(C)")
        else:
            age_withbirth.append(f"{meta1.loc[i, 'Env']}(V)")
    meta1['Env'] = age_withbirth
    meta1 = meta1.fillna(0)
    meta1.to_csv('meta_withbirth.csv', index=0)
    
    
        
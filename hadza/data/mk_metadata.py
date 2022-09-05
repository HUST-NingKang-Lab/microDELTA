import pandas as pd
import re
from sklearn.model_selection import KFold

table_s1 = pd.read_csv('aan4834_table_s1.csv', index_col = 0).loc["Smits, SA"].reset_index()
report = pd.read_csv('filereport_read_run_PRJNA392012_tsv.txt', sep = '\t')[['run_accession','sample_alias']]
report['sample_alias'] = report['sample_alias'].apply(lambda x: int(re.findall('\d+', x)[0]))
metadata = table_s1[['#SampleID', 'COLLECTION_DATE','Age', 'SEASON']]
report.set_index('sample_alias', inplace =True)
metadata['#SampleID'] = metadata['#SampleID'].apply(lambda x: report.loc[int(x)])
metadata.rename(columns = {'#SampleID': 'SampleID'}, inplace = True)
abundance = pd.read_csv('./abundance.csv', index_col = 0)

metadata_binary = metadata.copy()
metadata_binary['SEASON'] = metadata_binary['SEASON'].apply(lambda x: 'root:D' if 'D' in x else 'root:W')

metadata.to_csv('metadata.csv', index = False)
metadata_binary.to_csv('metadata_binary.csv', index = False)

# 8fold
meta_run = metadata_binary[['SampleID', 'SEASON']].set_index('SampleID').rename(columns = {'SEASON': 'Env'})
kf = KFold(n_splits = 8, shuffle = True, random_state = 1)

fold = 0
for source_index, query_index in kf.split(meta_run):
    source_meta, query_meta = meta_run.iloc[source_index], meta_run.iloc[query_index]
    source_meta.to_csv(f'../experiments/exp_{fold}/SourceMapper.csv')
    query_meta.to_csv(f'../experiments/exp_{fold}/QueryMapper.csv')
    source, query = abundance[source_meta.index], abundance[query_meta.index]
    source.to_csv(f'../experiments/exp_{fold}/SourceCM.tsv', sep = '\t')
    query.to_csv(f'../experiments/exp_{fold}/QueryCM.tsv', sep = '\t')
    fold += 1
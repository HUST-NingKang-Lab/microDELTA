import pandas as pd
import re

table_s1 = pd.read_csv('aan4834_table_s1.csv', index_col = 0).loc["Smits, SA"].reset_index()
report = pd.read_csv('filereport_read_run_PRJNA392012_tsv.txt', sep = '\t')[['run_accession','sample_alias']]
report['sample_alias'] = report['sample_alias'].apply(lambda x: int(re.findall('\d+', x)[0]))
metadata = table_s1[['#SampleID', 'COLLECTION_DATE','Age', 'SEASON']]
report.set_index('sample_alias', inplace =True)
metadata['#SampleID'] = metadata['#SampleID'].apply(lambda x: report.loc[int(x)])
metadata.rename(columns = {'#SampleID': 'SampleID'}, inplace = True)

metadata['Age'] = metadata['Age'].astype(float)
metadata_age = metadata[(metadata['Age'] >= 18) & (metadata['Age'] < 50)]
metadata_binary = metadata_age.copy()
metadata_binary['SEASON'] = metadata_binary['SEASON'].apply(lambda x: 'D' if 'D' in x else 'W')

metadata_age.to_csv('metadata.csv', index = False)
metadata_binary.to_csv('metadata_binary.csv', index = False)
metadata_age
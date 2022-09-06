import os
import pandas as pd


if __name__ == '__main__':
    # os.mkdir('5-years')
    # os.mkdir('12-months')
    # os.mkdir('5-years/cesarean-section')
    # os.mkdir('5-years/vaginal-delivery')
    # os.mkdir('12-months/cesarean-section')
    # os.mkdir('12-months/vaginal-delivery')
    
    metadata_withbirth = pd.read_csv('meta_withbirth.csv')
    metadata = pd.read_csv('metadata.csv')
    abundance = pd.read_csv('abundance.csv')
    
    C_index = []
    C_12M_queries = []
    C_5Y_queries = []
    C_12M_sources = []
    C_5Y_sources = []
    
    for i in metadata_withbirth.index:
        if ':C' in metadata_withbirth.loc[i, 'Env']:
            C_index.append(i)
    C_metadata = metadata.loc[C_index]
    C_metadata.columns = ['SampleID', 'Env']
    C_abundance = abundance[C_metadata['SampleID']]
    C_abundance.insert(0, 'Samples', abundance['Samples'])
    
    for i in C_metadata.index:
        if '5Y' in C_metadata.loc[i, 'Env']:
            C_5Y_queries.append(i)
        elif '12M' in C_metadata.loc[i, 'Env']:
            C_12M_queries.append(i)
            C_5Y_sources.append(i)
        else:
            C_12M_sources.append(i)
            C_5Y_sources.append(i)
            
    C_12M_sources_metadata = metadata.loc[C_12M_sources]      
    C_12M_sources_metadata.columns = ['SampleID', 'Env']
    C_12M_sources_abundance = abundance[C_12M_sources_metadata['SampleID']]
    C_12M_sources_abundance.insert(0, 'Samples', abundance['Samples'])
    
    C_5Y_sources_metadata = metadata.loc[C_5Y_sources]      
    C_5Y_sources_metadata.columns = ['SampleID', 'Env']
    C_5Y_sources_abundance = abundance[C_5Y_sources_metadata['SampleID']]
    C_5Y_sources_abundance.insert(0, 'Samples', abundance['Samples'])
    
    C_12M_metadata = metadata.loc[C_12M_queries]      
    C_12M_metadata.columns = ['SampleID', 'Env']
    C_12M_abundance = abundance[C_12M_metadata['SampleID']]
    C_12M_abundance.insert(0, 'Samples', abundance['Samples'])
    
    C_5Y_metadata = metadata.loc[C_5Y_queries]      
    C_5Y_metadata.columns = ['SampleID', 'Env']
    C_5Y_abundance = abundance[C_5Y_metadata['SampleID']]
    C_5Y_abundance.insert(0, 'Samples', abundance['Samples'])
    
    V_index = []
    V_12M_queries = []
    V_5Y_queries = []
    V_12M_sources = []
    V_5Y_sources = []
    
    for i in metadata_withbirth.index:
        if ':V' in metadata_withbirth.loc[i, 'Env']:
            V_index.append(i)
    V_metadata = metadata.loc[V_index]
    V_metadata.columns = ['SampleID', 'Env']
    metadata['Env'] = metadata['Env'].apply(lambda x: f'root:{x}')
    V_abundance = abundance[V_metadata['SampleID']]
    V_abundance.insert(0, 'Samples', abundance['Samples'])
    
    for i in V_metadata.index:
        if '5Y' in V_metadata.loc[i, 'Env']:
            V_5Y_queries.append(i)
        elif '12M' in V_metadata.loc[i, 'Env']:
            V_12M_queries.append(i)
            V_5Y_sources.append(i)
        else:
            V_12M_sources.append(i)
            V_5Y_sources.append(i)
            
    V_12M_sources_metadata = metadata.loc[V_12M_sources]      
    V_12M_sources_metadata.columns = ['SampleID', 'Env']
    V_12M_sources_abundance = abundance[V_12M_sources_metadata['SampleID']]
    V_12M_sources_abundance.insert(0, 'Samples', abundance['Samples'])
    
    V_5Y_sources_metadata = metadata.loc[V_5Y_sources]      
    V_5Y_sources_metadata.columns = ['SampleID', 'Env']
    V_5Y_sources_abundance = abundance[V_5Y_sources_metadata['SampleID']]
    V_5Y_sources_abundance.insert(0, 'Samples', abundance['Samples'])
    
    V_12M_metadata = metadata.loc[V_12M_queries]      
    V_12M_metadata.columns = ['SampleID', 'Env']
    V_12M_abundance = abundance[V_12M_metadata['SampleID']]
    V_12M_abundance.insert(0, 'Samples', abundance['Samples'])
    
    V_5Y_metadata = metadata.loc[V_5Y_queries]      
    V_5Y_metadata.columns = ['SampleID', 'Env']
    V_5Y_abundance = abundance[V_5Y_metadata['SampleID']]
    V_5Y_abundance.insert(0, 'Samples', abundance['Samples'])
    
    metadata.to_csv('5-years/cesarean-section/metadata.csv', index=0)
    metadata.to_csv('5-years/vaginal-delivery/metadata.csv', index=0)
    metadata.to_csv('12-months/cesarean-section/metadata.csv', index=0)
    metadata.to_csv('12-months/vaginal-delivery/metadata.csv', index=0)
    
    C_5Y_abundance.to_csv('5-years/cesarean-section/queries.tsv', sep='\t', index=0)
    C_12M_abundance.to_csv('12-months/cesarean-section/queries.tsv', sep='\t', index=0)
    C_5Y_sources_abundance.to_csv('5-years/cesarean-section/sources.tsv', sep='\t', index=0)
    C_12M_sources_abundance.to_csv('12-months/cesarean-section/sources.tsv', sep='\t', index=0)
    
    V_5Y_abundance.to_csv('5-years/vaginal-delivery/queries.tsv', sep='\t', index=0)
    V_12M_abundance.to_csv('12-months/vaginal-delivery/queries.tsv', sep='\t', index=0)
    V_5Y_sources_abundance.to_csv('5-years/vaginal-delivery/sources.tsv', sep='\t', index=0)
    V_12M_sources_abundance.to_csv('12-months/vaginal-delivery/sources.tsv', sep='\t', index=0)
    

    
    
          
    
    
    
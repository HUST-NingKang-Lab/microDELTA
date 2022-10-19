import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from plotnine import*
import matplotlib

def TransToDestination(x):
    if 'TT' in x:
        return 'TT'
    else:
        return 'BJN'

def RF(X_train, y_train, X_test):
    rfc = RandomForestClassifier(random_state = 61)
    rfc.fit(X_train, y_train)
    y_prob = rfc.predict_proba(X_test)
    df = pd.DataFrame(y_prob, columns = ['BJN', 'TT'], index = X_test.index)
    return df

abundance = pd.read_csv('../dataFiles/countmatrix.csv')
abundance['#OTU ID'] = abundance['#OTU ID'].apply(lambda x: np.nan if 'Other' in x else x)
abundance = abundance.dropna().set_index('#OTU ID').T

metadata = pd.read_csv('../dataFiles/metadata.csv', index_col = 0)
meta_position = metadata[['Treatment','People']]
meta_position['Treatment'] = meta_position['Treatment'].apply(TransToDestination)
meta_no_MT10 = meta_position[meta_position['People'] != 'MT10']    # For source

# Leve individual out
individuals = ['MT1', 'MT2', 'MT3','MT4', 'MT5', 'MT6', 'MT7', 'MT8', 'MT9', 'MT10']
result_df = pd.DataFrame(columns = ['BJN', 'TT']).astype(float)

for exp, i in enumerate(individuals):
    train_index = meta_no_MT10[meta_no_MT10['People'] != i].index
    test_index = meta_position[meta_position['People'] == i].index
    X_train, y_train = abundance.loc[train_index], meta_position.loc[train_index, 'Treatment']
    X_test, y_test = abundance.loc[test_index], meta_position.loc[test_index, 'Treatment']
    # Export data for transfer
    # X_train.T.to_csv(f'../experiments_repeat/exp_{exp+1}/SourceCM.tsv', sep = '\t')
    # X_test.T.to_csv(f'../experiments_repeat/exp_{exp+1}/QueryCM.tsv', sep = '\t')
    # y_train.apply(lambda x: f'root:{x}').rename('Env').rename_axis('SampleID').to_csv(f'../experiments_repeat/exp_{exp+1}/SourceMapper.csv')
    # y_test.apply(lambda x: f'root:{x}').rename('Env').rename_axis('SampleID').to_csv(f'../experiments_repeat/exp_{exp+1}/QueryMapper.csv')
    result_df = pd.concat([result_df, RF(X_train, y_train, X_test)])

result_df.to_csv('RF_result.csv')

# Plot
matplotlib.rcParams['pdf.fonttype'] = 42

suffix = 'Transfer_DM'
contributions = result_df
metadata = pd.read_csv('dataFiles/metadata.csv').set_index('#SampleID')
contributions = contributions.join(metadata, how='left')
#contributions = contributions[contributions.Phase != 'T6']
#data = contributions.groupby(by=['People', 'Phase'], as_index=False).mean()
contributions['GroupAll'] = '1'
contributions = contributions.sort_values('Timepoint')
contributions['Timepoint_str'] = contributions['Timepoint'].astype(str)
contributions['is_MT10'] = (contributions.People == 'MT10').map({True: 'MT10', False: 'MT1-9'})
data = contributions
data.loc[data.Phase=='T1', 'G'] = 'Before travel'
data.loc[data.Phase.isin(['T2', 'T3', 'T4']), 'G'] = 'During travel'
data.loc[data.Phase.isin(['T5', 'T6']), 'G'] = 'After travel'
T_unique = contributions[['Phase', 'Timepoint']].drop_duplicates()
contributions['Period'] = contributions.Phase.map(T_unique.Phase.value_counts(sort=False).to_dict())
contributions['Status (MT10)'] = 'Normal'
contributions.loc[(contributions.People == 'MT10')&(contributions.Timepoint > 15)&(contributions.Timepoint < 21), 'Status (MT10)'] = 'Early back'

plot = (ggplot(data, aes(x='Timepoint_str', y='TT'))
        + geom_boxplot(aes(fill='G', group='Timepoint_str'), outlier_shape='', show_legend=True, data=data[data.People != 'MT10'], width=0.5)
        #+ geom_violin(aes(fill='Phase', group='Timepoint_str'), show_legend=True, data=data[data.People != 'MT10'], bw=0.1)
        + scale_fill_manual(["#4DBBD5FF", "#00A087FF", "#3C5488FF", "#F39B7FFF", "#8491B4FF", "#91D1C2FF", "#DC0000FF", "#7E6148FF", "#B09C85FF"])
        #+ geom_boxplot(aes(group='Timepoint_str'), fill='white', alpha=0.5, show_legend=False, outlier_shape='', data=data[data.People != 'MT10'], width=0.4)
        + geom_smooth(aes(linetype='is_MT10', group='is_MT10'), se=False, method='loess', show_legend=True)
        + scale_linetype_manual(['solid', 'dashdot'])
        + geom_point(aes(color='Status (MT10)'), data=data[data.People == 'MT10'])
        + scale_color_manual(['brown', "black"])
        + theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank(),
             axis_line_x = element_line(color="gray", size = 1), axis_line_y = element_line(color="gray", size = 1))
        + geom_hline(yintercept=0.5, linetype="dotted")
        + geom_vline(xintercept=[2.5, 20.5], linetype="dashed", size=0.6)
        #+ geom_label(data='Early back', position=[15.5, 0.2])
        + scale_x_discrete(limits=contributions['Timepoint_str'].unique())
        + xlab('Time point')
        + ylab('Contribution from "Trinidad and Tobago"')
)

print(plot)
plot.save('Figure.pdf'.format('RF'), dpi=120, width=6.4*1.5, height=4.8)

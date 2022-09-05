import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from plotnine import*
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42

def RF(X_train, y_train, X_test):
    rfc = RandomForestClassifier(random_state = 5)
    rfc.fit(X_train, y_train)
    y_prob = rfc.predict_proba(X_test)
    df = pd.DataFrame(y_prob, columns = ['root:D', 'root:W'], index = X_test.index)
    return df

result_df = pd.DataFrame(columns = ['root:D', 'root:W'])

for i in range(8):
    source = pd.read_csv(f'../experiments/exp_{i}/SourceCM.tsv', sep = '\t', index_col = 0).T
    query = pd.read_csv(f'../experiments/exp_{i}/QueryCM.tsv', sep = '\t', index_col = 0).T
    source_meta = pd.read_csv(f'../experiments/exp_{i}/SourceMapper.csv', index_col = 0)
    result_df = pd.concat([result_df, RF(source, source_meta, query)])

metadata = pd.read_csv('../data/metadata.csv').set_index('SampleID')
metadata['COLLECTION_DATE'] = pd.to_datetime(metadata.COLLECTION_DATE)
metadata['COLLECTION_DATE_'] = metadata.COLLECTION_DATE.dt.year.astype(str) + '-' + \
    metadata.COLLECTION_DATE.dt.month.astype(str).str.rjust(2, '0') + '-' + \
    metadata.COLLECTION_DATE.dt.day.astype(str).str.rjust(2, '0')
sorted_months = metadata.COLLECTION_DATE.sort_values().copy()

result_df = result_df.join(metadata, how='left')
result_df['group'] = 'reference'
result_df['realdata'] = True
result_df['SEASON_'] = result_df['SEASON'].apply(lambda x: x.split('-')[1])
result_df['root:D'] = result_df['root:D'].astype(float)

plot = (ggplot(result_df, aes(x='COLLECTION_DATE_', y='root:D'))
        # + geom_rect(xmin=4.5, xmax=8.5, ymin=0.2, ymax=1.0, alpha=0.1, color='gray', linetype='dashed', size=0.4, fill='lightgray')
        + geom_boxplot(aes(fill='SEASON_', group='COLLECTION_DATE_'), show_legend=True, width=0.5)
        + scale_fill_manual(['khaki','lightgreen','gold','yellowgreen'], name = "Season", labels = ["Early Dry", "Early Wet", "Late Dry", "Late Wet"])
        #+ scale_fill_discrete(name = "Season", labels = ["Early Dry", "Early Wet", "Late Dry", "Late Wet"])
        #+ geom_boxplot(aes(group='Timepoint_str'), fill='white', alpha=0.5, show_legend=False, outlier_shape='', data=data[data.People != 'MT10'], width=0.4)
        + geom_smooth(aes(group='group'), se=True, method='loess', show_legend=True)
        #+ scale_linetype_manual(['solid', 'dashdot'])
        #+ geom_point(aes(color='SEASON_'), shape='o')
        
        #+ geom_point(color='red', data=c2, shape='o', size=3)
        #+ scale_color_manual(['brown', "black"])
        + theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank(),
             axis_line_x = element_line(color="gray", size = 1), axis_line_y = element_line(color="gray", size = 1),
             axis_text_x=element_text(rotation=-30, hjust=0.5))
        #+ geom_hline(yintercept=, linetype="dotted")
        #+ geom_vline(xintercept=[4.5, 8.5], linetype="dashed", size=0.6)
        #+ geom_label(data='Early back', position=[15.5, 0.2])
        #+ scale_x_discrete(limits=['2013-LD', '2014-EW', '2014-LW', '2014-ED', '2014-LD'])
        + xlab('Date')
        + ylab('Contribution from season: "Dry"')
)

print(plot)
plot.save('RF_figure.pdf', dpi=120, width=6.4*1.2, height=4.8)
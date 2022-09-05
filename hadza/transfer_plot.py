import os
import numpy as np
import pandas as pd
import matplotlib
from plotnine import *
matplotlib.rcParams['pdf.fonttype'] = 42

metadata = pd.read_csv('./data/metadata.csv').set_index('SampleID')
metadata['COLLECTION_DATE'] = pd.to_datetime(metadata.COLLECTION_DATE)
metadata['COLLECTION_DATE_'] = metadata.COLLECTION_DATE.dt.year.astype(str) + '-' + \
    metadata.COLLECTION_DATE.dt.month.astype(str).str.rjust(2, '0') + '-' + \
    metadata.COLLECTION_DATE.dt.day.astype(str).str.rjust(2, '0')
sorted_months = metadata.COLLECTION_DATE.sort_values().copy()

c1 = pd.concat([pd.read_csv('experiments/exp_{}/Search_Transfer_DM/layer-2.csv'.format(i), index_col=0) for i in range(8)])
#c2 = pd.concat([pd.read_csv('experiments/exp_{}/Search_Transfer_DM/layer-2.csv'.format(i), index_col=0).join(metadata, how='left').rename(index=lambda x: x+'_exp'+str(i)) for i in range(5)])

c1 = c1.join(metadata, how='left')
c1['group'] = 'reference'
c1['realdata'] = True
c1['SEASON_'] = c1['SEASON'].apply(lambda x: x.split('-')[1])

plot = (ggplot(c1, aes(x='COLLECTION_DATE_', y='root:D'))
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
plot.save('transfer_figure.pdf', dpi=120, width=6.4*1.2, height=4.8)
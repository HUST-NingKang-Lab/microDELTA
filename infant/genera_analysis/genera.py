from curses import color_content
from matplotlib import units
import matplotlib
import pandas as pd
import numpy as np
from plotnine import*

abundance =  pd.read_csv('../8folds/abundance.csv', index_col = 0)
file_report = pd.read_csv('../file_report.txt', sep = '\t', index_col = 1)['sample_alias']
metadata = pd.read_csv('../8folds/metadata.csv', index_col = 0)
file_report = file_report.loc[set(metadata.index) & set(file_report.index)]

# Filter samples that collected along complete series
file_report = file_report.str.split('-', expand = True)
samples_group_count = file_report[file_report[1] != 'M'].groupby(0).count()
target_index = samples_group_count[samples_group_count == 5].dropna().index    # 120 samples

report_reindex = file_report.reset_index().set_index(0)
target_id = report_reindex[report_reindex[1] != 'M'].loc[target_index]['run_accession']
target_metadata = report_reindex.set_index('run_accession', drop = True).loc[target_id]
target_metadata.rename(columns = {1: 'Env'}, inplace = True)
target_abundance = abundance[target_metadata.index]

# Group the trajectory
trajectory_1 = ['Bifidobacterium',
                'Enterococcus',
                'Lactobacillus',
                'Streptococcus',
                'Enterobacteriaceae',
                'Rothia',
                'Veillonella']

trajectory_2 = ['[Ruminococcus]',
                '[Eubacterium]',
                'Eggerthella',
                'Fusobacterium',
                'Haemophilus']

trajectory_3 = ['Bacteroides',
                'Faecalibacterium',
                'Roseburia',
                'Akkermansia',
                'Prevotella',
                'Ruminococcus',
                'Lachnospiraceae']

trajectory_4 = ['Methanobrevibacter',
                'Coriobacteriaceae',
                'Desulfovibrio',
                'Christensenellaceae',
                'cc_115',
                'S24-7',
                'Catenibacterium']

# Sum each age group
def SumByAge(age):
    age_id = target_metadata[target_metadata['Env'] == age].index
    return(target_abundance[age_id].sum(axis = 1))

age_df = pd.concat([SumByAge('NB'), 
                    SumByAge('4M'),
                    SumByAge('12M'),
                    SumByAge('3Y'),
                    SumByAge('5Y')], ignore_index = True, axis = 1)

age_df.columns = ['NB', '4M', '12M', '3Y', '5Y']

# Calculate each genera in all samples
def CalculateTrajectory(trajectory):
    trajectory_df = pd.DataFrame(np.zeros((len(trajectory), 5)), 
                                 columns = ['NB', '4M', '12M', '3Y', '5Y'],
                                 index = trajectory)
    for genera in trajectory:
        for tax in target_abundance.index:
            if genera in tax:
                trajectory_df.loc[genera] += age_df.loc[tax]

    return (trajectory_df/120).reset_index(drop = False).melt(id_vars = 'index', var_name = 'Age', value_name = 'Abundance')
        
    
plot_df_1 = CalculateTrajectory(trajectory_1)
plot_df_2 = CalculateTrajectory(trajectory_2)
plot_df_3 = CalculateTrajectory(trajectory_3)
plot_df_4 = CalculateTrajectory(trajectory_4)

# Plot
plot_1 = (ggplot(plot_df_1, aes(x = 'Age', y = 'Abundance', linetype = 'index', color = 'index', group = 'index')) +
            # geom_point(aes(fill = 'index', color = 'index')) +
            geom_line() +
            scale_y_log10() +
            scale_color_manual(['#E7F0CA', '#63703C', '#E7F0CA', '#63703C', '#E7F0CA', '#63703C', '#E7F0CA']) +
            scale_linetype_manual(['-', '-', '--', '--', '-.', '-.', ':']) +
            xlim(['NB', '4M', '12M', '3Y', '5Y']) +
            ylab('Mean log10 relative abundance') +
            theme_bw() +
            theme(legend_title = element_blank(),
                    text = element_text(size = 10),
                    axis_text = element_text(size = 10, color = 'black'),
                    panel_grid_major = element_blank(),
                    panel_grid_minor = element_blank()))

plot_1.save('trajectory_1.jpg', height = 70, width = 100, units = ('mm'), dpi = 300)

plot_2 = (ggplot(plot_df_2, aes(x = 'Age', y = 'Abundance', linetype = 'index', color = 'index', group = 'index')) +
            # geom_point(aes(fill = 'index', color = 'index')) +
            geom_line() +
            scale_y_log10() +
            scale_color_manual(['#706C4B', '#F0E159', '#706C4B', '#F0E159', '#706C4B', '#F0E159', '#706C4B']) +
            scale_linetype_manual(['-', '-', '--', '--', '-.', '-.', ':']) +
            xlim(['NB', '4M', '12M', '3Y', '5Y']) +
            ylab('Mean log10 relative abundance') +
            theme_bw() +
            theme(legend_title = element_blank(),
                    text = element_text(size = 10),
                    axis_text = element_text(size = 10, color = 'black'),
                    panel_grid_major = element_blank(),
                    panel_grid_minor = element_blank()))

plot_2.save('trajectory_2.jpg', height = 70, width = 100, units = ('mm'), dpi = 300)

plot_3 = (ggplot(plot_df_3, aes(x = 'Age', y = 'Abundance', linetype = 'index', color = 'index', group = 'index')) +
            # geom_point(aes(fill = 'index', color = 'index')) +
            geom_line() +
            scale_y_log10() +
            scale_color_manual(['#57231B', '#DD9287', '#57231B', '#DD9287', '#57231B', '#DD9287', '#57231B']) +
            scale_linetype_manual(['-', '-', '--', '--', '-.', '-.', ':']) +
            xlim(['NB', '4M', '12M', '3Y', '5Y']) +
            ylab('Mean log10 relative abundance') +
            theme_bw() +
            theme(legend_title = element_blank(),
                    text = element_text(size = 10),
                    axis_text = element_text(size = 10, color = 'black'),
                    panel_grid_major = element_blank(),
                    panel_grid_minor = element_blank()))

plot_3.save('trajectory_3.jpg', height = 70, width = 100, units = ('mm'), dpi = 300)

plot_4 = (ggplot(plot_df_4, aes(x = 'Age', y = 'Abundance', linetype = 'index', color = 'index', group = 'index')) +
            # geom_point(aes(fill = 'index', color = 'index')) +
            geom_line() +
            scale_y_log10() +
            scale_color_manual(['#1C4E57', '#89D0DD', '#1C4E57', '#89D0DD', '#1C4E57', '#89D0DD', '#1C4E57']) +
            scale_linetype_manual(['-', '-', '--', '--', '-.', '-.', ':']) +
            xlim(['NB', '4M', '12M', '3Y', '5Y']) +
            ylab('Mean log10 relative abundance') +
            theme_bw() +
            theme(legend_title = element_blank(),
                    text = element_text(size = 10),
                    axis_text = element_text(size = 10, color = 'black'),
                    panel_grid_major = element_blank(),
                    panel_grid_minor = element_blank()))

plot_4.save('trajectory_4.jpg', height = 70, width = 100, units = ('mm'), dpi = 300)


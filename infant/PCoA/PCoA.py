import pandas as pd
from skbio.stats.ordination import pcoa
from skbio.diversity import beta_diversity
from plotnine import*



if __name__ == '__main__':
    abundance = pd.read_csv('../8folds/abundance.csv', index_col = 0).T
    metadata = pd.read_csv('../8folds/metadata.csv').set_index('SampleID')

    distance_mat = beta_diversity('braycurtis', abundance, ids = metadata.index.tolist())
    pcoa_result = pcoa(distance_mat, number_of_dimensions=2)
    pcoa_df = pd.DataFrame(pcoa(distance_mat, number_of_dimensions=2).samples.values.tolist(), 
                            columns = ['PC1', 'PC2'], index = abundance.index)
    
    pcoa_plot = (ggplot(pcoa_df, aes(x = 'PC1', y = 'PC2', fill = metadata)) +
                    geom_point() +
                    xlim(-0.6, 0.6) +
                    ylim(-0.6, 0.6) +
                    theme(panel_grid_major = element_blank(), 
							panel_grid_minor = element_blank(), 
							panel_background = element_blank()) +
			        theme(axis_line = element_line(color="gray", size = 1)) +
                    theme(legend_title = element_blank()) +
			        xlab('PC1') +
			        ylab('PC2'))
    
    pcoa_plot.save('PCoA.png')

    box_1 = (ggplot(pcoa_df, aes(x=metadata, y='PC1', fill=metadata))
			+ geom_boxplot(width=0.3, show_legend=False)
			#+ scale_color_manual(['#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF','#F39B7FFF','#8491B4FF','#91D1C2FF'])
			+ theme(figure_size=[4.8, 2])
			+ theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())
			+ theme(axis_line = element_line(color="black", size = 1))
			+ xlab('')
			+ ylab('PC1')
			+ coord_flip()
   			+ xlim(['B', '4M', '12M', '3Y', '5Y', 'M'])
		   )
    box_1.save('PC1_box.png')

    box_2 = (ggplot(pcoa_df, aes(x=metadata, y='PC2', fill=metadata))
			+ geom_boxplot(width=0.3, show_legend=False)
			#+ scale_color_manual(['#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF','#F39B7FFF','#8491B4FF','#91D1C2FF'])
			+ theme(figure_size=[2, 4.8])
			+ theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())
			+ theme(axis_line = element_line(color="black", size = 1))
			+ xlab('')
			+ ylab('PC2')
			+ xlim(['B', '4M', '12M', '3Y', '5Y', 'M'])
		   )
    box_2.save('PC2_box.png')
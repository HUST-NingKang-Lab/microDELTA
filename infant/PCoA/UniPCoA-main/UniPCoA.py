import os
import pandas as pd
from plotnine import *
import plotnine
from matplotlib import pyplot as plt
import matplotlib
from scipy.spatial.distance import pdist, squareform
from skbio.stats.ordination import pcoa
from skbio.diversity import beta_diversity
from skbio.io import read
from skbio.tree import TreeNode
import argparse
from scipy.spatial.distance import pdist, squareform


def loadTree(tree):
	with open(tree, 'r') as f: 
		tree = read(f, format="newick", into=TreeNode)
	return tree


if __name__ == '__main__':
	matplotlib.rcParams['pdf.fonttype'] = 42
	matplotlib.rcParams['ps.fonttype'] = 42
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--abundance', type=str, default='species_abundance.csv', help='The input abundance data, columns represent samples and rows represent taxa.')
	parser.add_argument('-m', '--metadata', type=str, default='metadata.csv', help='The input metadata, use column "Env" to specify the group of the input samples.')
	parser.add_argument('-o', '--output', type=str, default='PLots.Unifrac', help='The folder to save output table and plots.')
	parser.add_argument('-t', '--tree', type=str, default='LTPs132_SSU_tree.newick', help='The input phylogenetic tree, in Newick format.')
	parser.add_argument('--metric', type=str, default='weighted_unifrac', help='The metric for beta_diversity calculation.')
	args = parser.parse_args()
	print('Loading data...')
	X = pd.read_csv(args.abundance, index_col=0).T
	Y = pd.read_csv(args.metadata).set_index('SampleID')
	use_phylogeny = args.metric in ['weighted_unifrac', 'unweighted_unifrac']
	if use_phylogeny:
		tree = loadTree(tree=args.tree)
		print('Processing the phylogenetic tree...')
		for n in tree.postorder():
			if n.name != None and '_ ' in n.name:
				n.name = n.name.split('_ ')[1]
		names = [n.name for n in tree.postorder()]
	print('Processing the abundance data...')
	ids = X.index.tolist()
	otu_ids = X.columns.tolist()
	X = X.reset_index().melt(id_vars=['index'], value_vars=X.columns, var_name='taxonomy', value_name='abundance')
	taxa = pd.DataFrame(X.taxonomy.apply(lambda x: dict(map(lambda y: y.split('__'), filter(lambda x: not x.endswith('__'), x.split(';'))))).tolist())
	X = pd.concat([X.drop(columns=['taxonomy']), taxa], axis=1)
	X = X.melt(id_vars=['index','abundance'], value_vars=taxa.columns, var_name='rank', value_name='taxonomy')
	X = X.groupby(by=['index', 'taxonomy'], as_index=False).sum().pivot_table(columns='taxonomy', index='index', values='abundance')
	if use_phylogeny:
		X = X.loc[:, X.columns.to_series().isin(names)]
	ids = X.index.tolist()
	otu_ids = X.columns.tolist()
	
	try:
		print('Trying calculating {} beta_diversity using scikit-bio & scikit-learn package...'.format(args.metric))
		print('This could be time-consuming.')
		if use_phylogeny:
			mat = beta_diversity(args.metric, X, ids, tree=tree, otu_ids=otu_ids, validate=False).data
		else:
			mat = beta_diversity(args.metric, X, ids, otu_ids=otu_ids, validate=False).data
	except ValueError:
		print('Failed, the metric you selected is not supported by neither scikit-bio nor scikit-learn.')
		print('Trying using SciPy...')
		mat = squareform(pdist(X, metric=args.metric))
	print('Succeeded!')
	df = pd.DataFrame(mat)
	df.to_csv('distance.csv', index=0)
	pcs = pd.DataFrame(pcoa(mat, number_of_dimensions=2).samples.values.tolist(), index=X.index, columns=['PC1', 'PC2'])
	pcs = pd.concat([pcs, Y], axis=1)
	print('Visualizing the data using plotnine package...')
	print(pcs)
	p = (ggplot(pcs, aes(x='PC1', y='PC2', color='Env'))
			+ geom_point(size=0.2)
			#+ scale_color_manual(['#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF','#F39B7FFF','#8491B4FF','#91D1C2FF'])
			+ theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())
			+ theme(axis_line = element_line(color="gray", size = 1))
			+ stat_ellipse()
			+ xlab('PC1')
			+ ylab('PC2')
		   )
	box_1 = (ggplot(pcs, aes(x='Env', y='PC1', color='Env'))
			+ geom_boxplot(width=0.3, show_legend=False)
			#+ scale_color_manual(['#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF','#F39B7FFF','#8491B4FF','#91D1C2FF'])
			+ theme(figure_size=[4.8, 1])
			+ theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())
			+ theme(axis_line = element_line(color="gray", size = 1))
			+ xlab('Env')
			+ ylab('PC1')
			+ coord_flip()
   			+ xlim(['B', '4M', '12M', '3Y', '5Y', 'M'])
		   )
	box_2 = (ggplot(pcs, aes(x='Env', y='PC2', color='Env'))
			+ geom_boxplot(width=0.3, show_legend=False)
			#+ scale_color_manual(['#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF','#F39B7FFF','#8491B4FF','#91D1C2FF'])
			+ theme(figure_size=[4.8, 1])
			+ theme(panel_grid_major = element_blank(), panel_grid_minor = element_blank(), panel_background = element_blank())
			+ theme(axis_line = element_line(color="gray", size = 1))
			+ xlab('Env')
			+ ylab('PC2')
			+ coord_flip()
			+ xlim(['B', '4M', '12M', '3Y', '5Y', 'M'])
		   )

	if not os.path.isdir(args.output):
		os.mkdir(args.output)
	p.save(os.path.join(args.output, 'PCoA.pdf'), width=4.8, height=4.8)
	box_1.save(os.path.join(args.output, 'PC1_boxplot.pdf'), width=4.8, height=1)
	box_2.save(os.path.join(args.output, 'PC2_boxplot.pdf'), width=4.8, height=1)
	pcs.to_csv(os.path.join(args.output, 'Principle_coordinations.csv'))
	print('Plots are saved in {}. Import them into Illustrator for further improvements.'.format(args.output))
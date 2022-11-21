from importlib.metadata import metadata
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve, auc
from plotnine import *

metadata = pd.concat([pd.read_csv(f'./experiments/exp_{i}/SourceMapper.csv',  
                                  index_col = 0) for i in range(8)])
metadata = metadata[~metadata.index.duplicated(keep='first')]

ground_truth = metadata['Env'].apply(lambda x: 1 if ':D' in x else 0)

tf_result = pd.concat([pd.read_csv(f'./experiments/exp_{i}/Search_Transfer_DM/layer-2.csv', 
                                   index_col = 0)['root:D'] for i in range(8)])
nn_result = pd.concat([pd.read_csv(f'./nn_result/exp_{i}/Search/layer-2.csv', 
                                   index_col = 0)['root:D'] for i in range(8)])

ground_truth = ground_truth[tf_result.index]
nn_result = nn_result[tf_result.index]


nn_fpr, nn_tpr, _ = roc_curve(ground_truth, nn_result, drop_intermediate = False)
nn_auc = auc(nn_fpr,nn_tpr)
nn_df = pd.DataFrame({'fpr': nn_fpr, 'tpr': nn_tpr, 'auc': nn_auc})
nn_df['method'] = 'Independent model'

tf_fpr, tf_tpr, _ = roc_curve(ground_truth, tf_result, drop_intermediate = False)
tf_auc = auc(tf_fpr, tf_tpr)
tf_df = pd.DataFrame({'fpr': tf_fpr, 'tpr': tf_tpr, 'auc': tf_auc})
tf_df['method'] = 'transfer model'

plot_df = pd.concat([nn_df, tf_df])

auc_fig = (ggplot(plot_df, aes(x = 'fpr', y = 'tpr', color = 'method')) +
    geom_line() +
    # geom_point() +
    geom_abline(intercept = 0, slope = 1) +
    annotate('text', label = 'independent AUROC = %.3f' % nn_auc, x = 0.7, y = 0.3, size = 5) +
    annotate('text', label = 'transfer AUROC = %.3f' % tf_auc, x = 0.78, y = 0.4, size = 5) +
    labs(x = 'False Positive Rate', y = 'True Positive Rate', title = 'AUROC of Hadza hunter-gatherer cohort') +
    theme_bw() +
    theme(text = element_text(size = 10),
            axis_text = element_text(size = 10, color = 'black'),
            axis_title = element_text(size = 10),
            legend_position = (0.72, 0.2),
            legend_entry_spacing_y = 5,
            legend_title = element_blank(),
            legend_text = element_text(size = 5),
            legend_key = element_blank(),
            legend_background = element_blank(),
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank()))

auc_fig.save('./auc.pdf', width = 70, dpi = 300, height = 70, units = 'mm')
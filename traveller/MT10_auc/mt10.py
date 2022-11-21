import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, average_precision_score
from plotnine import *

tf_result = pd.read_csv('../experiments/exp_10/Search_Transfer_DM/layer-2.csv', index_col = 0).sort_index()
nn_result = pd.read_csv('../nn_result/exp_10/Search/layer-2.csv', index_col = 0).loc[tf_result.index]
rf_result = pd.read_csv('../RF/RF_result.csv', index_col = 0).loc[tf_result.index]
ground_truth = np.zeros(rf_result.shape[0])
ground_truth[-9:] = 1 

nn_TT = nn_result.values[:, 1]
rf_TT = rf_result.values[:, 1]
tf_TT = tf_result.values[:, 1]

rf_fpr, rf_tpr, _ = roc_curve(ground_truth, rf_TT, drop_intermediate = False)
rf_auc = auc(rf_fpr, rf_tpr)
rf_df = pd.DataFrame({'fpr': rf_fpr, 'tpr': rf_tpr, 'auc': rf_auc})
# rf auc with three decimal places
rf_df['method'] = f'RF ({rf_auc:.3f})'

nn_fpr, nn_tpr, _ = roc_curve(ground_truth, nn_TT, drop_intermediate = False)
nn_auc = auc(nn_fpr, nn_tpr)
nn_df = pd.DataFrame({'fpr': nn_fpr, 'tpr': nn_tpr, 'auc': nn_auc})
nn_df['method'] = f'Neural Network ({nn_auc:.3f})'

tf_fpr, tf_tpr, _ = roc_curve(ground_truth, tf_TT, drop_intermediate = False)
tf_auc = auc(tf_fpr, tf_tpr)
tf_df = pd.DataFrame({'fpr': tf_fpr, 'tpr': tf_tpr, 'auc': tf_auc})
tf_df['method'] = f'microDELTA ({tf_auc:.3f})'

plot_df = pd.concat([tf_df, nn_df, rf_df])
order_catagory = pd.CategoricalDtype(categories = [f'microDELTA ({tf_auc:.3f})', 
                                                   f'Neural Network ({nn_auc:.3f})', 
                                                   f'RF ({rf_auc:.3f})'], ordered = True)
plot_df['method'] = plot_df['method'].astype(order_catagory)

auc_fig = (ggplot(plot_df, aes(x = 'fpr', y = 'tpr', color = 'method')) +
    geom_line() +
    geom_point() +
    geom_abline(intercept = 0, slope = 1) +
    # annotate('text', label = 'RF AUROC = %.3f' % rf_auc, x = 0.7, y = 0.3, size = 5) +
    # annotate('text', label = 'microDELTA AUROC = %.3f' % tf_auc, x = 0.78, y = 0.35, size = 5) +
    # annotate('text', label = 'Neural Network AUROC = %.3f' % nn_auc, x = 0.72, y = 0.4, size = 5) +
    labs(x = 'False Positive Rate', y = 'True Positive Rate', title = 'AUROC of MT10') +
    theme_bw() +
    theme(text = element_text(size = 10),
            axis_text = element_text(size = 10, color = 'black'),
            axis_title = element_text(size = 10),
            legend_position = (0.65, 0.2),
            # legend_entry_spacing_y = 2,
            legend_title = element_blank(),
            # legend_text = element_text(size = 5),
            legend_key = element_blank(),
            legend_background = element_blank(),
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank()))

auc_fig.save('./mt10_auc.pdf', width = 100, dpi = 300, height = 100, units = 'mm')



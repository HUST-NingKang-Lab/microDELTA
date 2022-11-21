import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score

def TransToLabel(x):
    if 'TT' in x:
        return '0'
    else:
        return '1'

metadata = pd.read_csv('../dataFiles/metadata.csv', index_col = 0)
meta_position = metadata[['Treatment','People']]
ground_truth = meta_position['Treatment'].apply(TransToLabel)

rf_result = pd.read_csv('../RF/RF_result.csv', index_col = 0)['BJN']
# tf_result = pd.concat([pd.read_csv(f'../experiments/exp_{i}/Search_Transfer_DM/layer-2.csv', index_col = 0)['root:China'] for i in range(1, 11)])
tf_result = pd.concat([pd.read_csv(f'../experiments_repeat/exp_{i}/Search_Transfer_DM/layer-2.csv', index_col = 0)['root:BJN'] for i in range(1, 11)])
nn_result = pd.concat([pd.read_csv(f'../nn_result/exp_{i}/Search/layer-2.csv', index_col = 0)['root:BJN'] for i in range(1, 11)])

ground_truth = ground_truth[tf_result.index]
rf_result = rf_result.loc[tf_result.index]
nn_result = nn_result[tf_result.index]

rf_auc = roc_auc_score(ground_truth, rf_result)
tf_auc = roc_auc_score(ground_truth, tf_result)
nn_auc = roc_auc_score(ground_truth, nn_result)
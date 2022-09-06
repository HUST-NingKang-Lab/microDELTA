import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_curve, auc  
from sklearn.preprocessing import label_binarize
from plotnine import*

def RF(X_train, y_train, X_test, y_test):
    rfc = OneVsRestClassifier(RandomForestClassifier(random_state = 5))
    rfc = rfc.fit(X_train, y_train)
    y_pred = rfc.predict_proba(X_test)

    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(11):
        fpr[labels[i]], tpr[labels[i]], _ = roc_curve(y_test[:, i], y_pred[:, i])
        roc_auc[labels[i]] = auc(fpr[labels[i]], tpr[labels[i]])
    return pd.DataFrame(roc_auc, columns = labels, index = X_test.index)

metadata = pd.read_csv('../meta_withbirth.csv', index_col = 0).replace({'M(C)': 'M', 'M(V)': 'M', 'B(C)': 'NB(C)', 'B(V)': 'NB(V)'})
abundance = pd.read_csv('../abundance.csv', index_col = 0).T
labels = ['NB(C)', 'NB(V)', '4M(C)', '4M(V)', '12M(C)', '12M(V)', '3Y(C)', '3Y(V)', '5Y(C)', '5Y(V)','M']

result = pd.DataFrame(columns = labels)
kf = KFold(n_splits = 8, shuffle = True, random_state = 5)
for train_index, test_index in kf.split(abundance):
    X_train, y_train = abundance.iloc[train_index], metadata.iloc[train_index]
    X_test, y_test = abundance.iloc[test_index], metadata.iloc[test_index]
    y_train = label_binarize(y_train, classes = labels)
    y_test = label_binarize(y_test, classes = labels)
    result = pd.concat([result, RF(X_train, y_train, X_test, y_test)])

result = result.melt(var_name = 'Env')
result['value'] = result['value'].astype(float)
p = (ggplot(result, aes(x = 'Env', y = 'value')) +
         geom_boxplot(fill = "#DC143C") +
         theme_bw() +
         xlim('NB(C)', 'NB(V)', '4M(C)', '4M(V)', '12M(C)', '12M(V)', '3Y(C)', '3Y(V)', '5Y(C)', '5Y(V)','M') +
         ylim(0, 1) +
         xlab('') +
         ylab('AUROC') +
         theme(text=element_text(size = 10),
        axis_text = element_text(size = 10, color = 'black'),
        panel_grid_major = element_blank(), 
        panel_grid_minor = element_blank(),
        legend_background = element_blank(),
        legend_title = element_blank(),
        legend_position = (0.92, 0.11)))
print(p)
p.save('RF_result.png', height = 100, width = 200, units = 'mm')
    
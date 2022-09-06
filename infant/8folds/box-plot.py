import pandas as pd
from plotnine import*


if __name__ == '__main__':
    independent_evaluation = pd.DataFrame()
    for i in range(8):
        independent_evaluation = pd.concat([independent_evaluation, pd.read_csv(f'group{i+1}/independent_evaluation/overall.csv')])
    independent_evaluation = independent_evaluation.reset_index().drop('index', axis=1)
    independent_evaluation.columns = ['Env', 'ROC-AUC', 'F-max']
    independent_evaluation['mode'] = 'independent'
    
    transfer_evaluation = pd.DataFrame()
    for i in range(8):
        transfer_evaluation = pd.concat([transfer_evaluation, pd.read_csv(f'group{i+1}/transfer_evaluation/overall.csv')])
    transfer_evaluation = transfer_evaluation.reset_index().drop('index', axis=1)
    transfer_evaluation.columns = ['Env', 'ROC-AUC', 'F-max']
    transfer_evaluation['mode'] = 'transfer'
    
    whole_evaluation = pd. concat([transfer_evaluation, independent_evaluation])
    # whole_evaluation.to_csv('plot-data.csv', index = 0)
    whole_evaluation = whole_evaluation.groupby('Env').filter(lambda x: ':V' in x)
    print(whole_evaluation)
    
    box_fig = (ggplot(whole_evaluation, aes(x='Env', y='ROC-AUC', fill='mode'))
               +geom_boxplot(show_legend=1)
               +xlim(['root:B','root:B:C','root:B:V','root:4M','root:4M:C','root:4M:V',
                           'root:12M','root:12M:C','root:12M:V','root:3Y','root:3Y:C','root:3Y:V',
                           'root:5Y','root:5Y:C','root:5Y:V','root:M']))
            
    print(box_fig)
        
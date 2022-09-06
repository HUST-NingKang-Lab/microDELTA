import pandas as pd
from plotnine import*

def df_median(df, mode):
     df_median = pd.DataFrame(list(zip(df.columns[1:],[df[i].median() for i in df.columns[1:]])), 
                                columns=['Env', 'Contribution'])
     df_median['mode'] = mode
     return(df_median)

def df_melt(df, mode):
     df_melt = df.melt(id_vars = 'Unnamed: 0', var_name = 'Env', value_name = 'Contribution')
     df_melt['mode'] = mode
     return(df_melt)

if __name__ == '__main__':
     C_12M =  pd.read_csv('12-months/cesarean-section/result/layer-2.csv')
     V_12M =  pd.read_csv('12-months/vaginal-delivery/result/layer-2.csv')
     C_5Y =  pd.read_csv('5-years/cesarean-section/result/layer-2.csv')
     V_5Y =  pd.read_csv('5-years/vaginal-delivery/result/layer-2.csv')    
    
     C_12M_median = df_median(C_12M, 'C')
     V_12M_median = df_median(V_12M, 'V')
     df_12M_median = pd.concat([C_12M_median, V_12M_median], ignore_index=True, axis=0)
     df_12M_median.to_csv('12M_median.csv', index=0)
    
     C_5Y_median = df_median(C_5Y, 'C')
     V_5Y_median = df_median(V_5Y, 'V')
     df_5Y_median = pd.concat([C_5Y_median, V_5Y_median], ignore_index=True, axis=0)
     df_5Y_median.to_csv('5Y_median.csv', index=0)
    
     C_12M_box = df_melt(C_12M, 'C')
     V_12M_box = df_melt(V_12M, 'V')
     df_12M_box = pd.concat([C_12M_box, V_12M_box], ignore_index=True, axis=0)
     df_12M_box.to_csv('12M_box.csv', index=0)
    
     C_5Y_box = df_melt(C_5Y, 'C')
     V_5Y_box = df_melt(V_5Y,'V')
     df_5Y_box = pd.concat([C_5Y_box, V_5Y_box], ignore_index=True, axis=0)
     df_5Y_box.to_csv('5Y_box.csv', index=0)
     
    
     p1 = (ggplot(df_12M_box, aes(x = 'Env', y = 'Contribution', fill = 'mode'))+
         geom_boxplot()+
         theme_bw()+
         xlim(['root:B', 'root:4M']))
    
     print(p1)
    
     p2 = (ggplot(df_5Y_box, aes(x = 'Env', y = 'Contribution', fill = 'mode'))+
         geom_boxplot()+
         theme_bw()+
         xlim(['root:B', 'root:4M', 'root:12M', 'root:3Y']))
     print(p2)

     p_12M_line = (ggplot(df_12M_median, aes(x = 'Env', y = 'Contribution', group = 'mode'))+
                   geom_line(color=['#008B8B', '#FF8C00'])+
                   geom_point()+
                   theme_bw()+
                   xlim(['root:B', 'root:4M']))
     print(p_12M_line)
     
     p_5Y_line = (ggplot(df_5Y_median, aes(x = 'Env', y = 'Contribution', color = 'mode'))+
                   geom_line()+
                   geom_point()+
                   theme_bw()+
                   xlim(['root:B', 'root:4M', 'root:12M', 'root:3Y']))
     print(p_5Y_line)
     
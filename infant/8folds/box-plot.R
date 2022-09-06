library(ggplot2)
library(ggpubr)
plot.data = read.csv('plot-data.csv')

p1 = ggplot(plot.data, aes(x=Env, y=ROC.AUC, fill=mode))+
  geom_boxplot()+
  scale_fill_manual(values = c("#DC143C", "#87CEEB"))+
  xlim(c('NB(C)', 'NB(V)', '4M(C)', '4M(V)', 
         '12M(C)', '12M(V)', '3Y(C)', '3Y(V)', '5Y(C)', '5Y(V)','M'))+
  theme_bw()+
  xlab('')+
  ylab('AUROC')+
  stat_compare_means(aes(label = ..p.signif..), 
                     hide.ns = TRUE,
                     method = "wilcox.test",
                     label.y = 0.95,
                     size =10
                     )+
  theme(text=element_text(size = 10),
        axis.text = element_text(size = 10, color = 'black'),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(),
        legend.background = element_blank(),
        legend.title = element_blank(),
        legend.position = c(0.92, 0.11))
p1

ggsave('r-plot-data.jpg', height = 100, width = 200, units = 'mm')

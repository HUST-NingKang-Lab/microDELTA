library(ggplot2)

df.12M.median = read.csv(file = '12M_median.csv')
p.12M.line = ggplot(data = df.12M.median, mapping = aes(x = Env, 
                                             y = Contribution, 
                                             group = mode,
                                             color = mode))+
  geom_line()+
  geom_point()+
  theme_bw()+
  xlim(c('root:B', 'root:4M'))
p.12M.line
ggsave('plot/12M_line.png')

df.5Y.median = read.csv(file = '5Y_median.csv')
p.5Y.line = ggplot(data = df.5Y.median, mapping = aes(x = Env, 
                                                        y = Contribution, 
                                                        group = mode,
                                                        color = mode))+
  geom_line()+
  geom_point()+
  theme_bw()+
  xlim(c('root:B', 'root:4M', 'root:12M', 'root:3Y'))
p.5Y.line
ggsave('plot/5Y_line.png')

df.12M.box = read.csv('12M_box.csv')
p.12M.box = ggplot(df.12M.box, aes(x = Env, 
                                   y = Contribution,
                                   fill = mode))+
  geom_boxplot()+
  theme_bw()+
  xlim(c('root:B', 'root:4M'))
p.12M.box
ggsave('plot/12M_box.png')

df.5Y.box = read.csv('5Y_box.csv')
p.5Y.box = ggplot(df.5Y.box, aes(x = Env, 
                                   y = Contribution,
                                   fill = mode))+
  geom_boxplot()+
  theme_bw()+
  xlim(c('root:B', 'root:4M', 'root:12M', 'root:3Y'))
p.5Y.box
ggsave('plot/5Y_box.png')

p.12M.combine = ggplot()+
  geom_boxplot(data = df.12M.box, mapping = aes(x = Env, 
                              y = Contribution,
                              fill = mode))+
  geom_line(data = df.12M.median, mapping = aes(x = Env, 
                                                y = Contribution,
                                                fill = mode))+
  geom_point(data = df.12M.median, mapping = aes(x = Env, 
                                                 y = Contribution,
                                                 fill = mode))+
  theme_bw()+
  xlim(c('root:B', 'root:4M'))
p.12M.combine
ggsave('plot/12M_combine.png')

p.5Y.combine = ggplot()+
  geom_boxplot(df.5Y.box, aes(x = Env, 
                               y = Contribution,
                               fill = mode))+
  geom_line()+
  geom_point()+
  theme_bw()+
  xlim(c('root:B', 'root:4M', 'root:12M', 'root:3Y'))
p.5Y.combine
ggsave('plot/5Y_combine.png')
  

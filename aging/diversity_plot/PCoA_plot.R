library(dplyr)
library(ggplot2)
library(vegan)
library(ape)
library(umap)

abundance_whole <- read.csv('../data_jiangsu_and_sichuan/abundance_whole.csv')[ ,-1]
meta_whole <- read.csv('../data_jiangsu_and_sichuan/metadata_whole.csv')
meta_region <- read.csv('../data_jiangsu_and_sichuan/region_whole.csv')

meta_no_cent <- meta_whole %>%
                mutate(Env = replace(Env, Env =='Elder', 'Senior')) %>%
                filter(Env != 'Centenarian')

region_no_cent <- meta_region %>%
                        filter(X.SampleID %in% meta_no_cent$X)

abundance_no_cent <- abundance_whole[meta_no_cent$X]

bray_dis <- vegdist(t(abundance_no_cent), method = 'bray')
pcoa_frame <- pcoa(bray_dis)
x_label<-round(pcoa_frame$values$Rel_corr_eig[1]*100,2)
y_label<-round(pcoa_frame$values$Rel_corr_eig[2]*100,2)
plot_frame <- data.frame(pcoa_frame$vectors)
meta_no_cent$Env <- factor(meta_no_cent$Env, levels = c('Young', 'Senior'))

PCoA_plot <- ggplot(plot_frame, aes(Axis.2, Axis.1, fill = meta_no_cent$Env, color = meta_no_cent$Env)) +
                geom_point(size=0.5) +
                stat_ellipse(show.legend = FALSE) +
                theme_bw() +
                scale_color_manual(values = c('#B24D5E', '#4D5EB2')) +
                xlim(-0.7, 0.7) +
                ylim(-0.7, 0.7) +
                xlab(paste0("PCoA1 ",x_label,"%")) +
                ylab(paste0("PCoA2 ",y_label,"%")) +
                theme(axis.text = element_text(size = 10, color = 'black'),
                        panel.grid.major = element_blank(), 
                        panel.grid.minor = element_blank(),
                        panel.background = element_blank(),
                        # legend.position = c(1.5, 1.5),
                        legend.key.size = unit(0.5, 'cm'),
                        legend.title = element_blank(),
                        text = element_text(size = 10))
ggsave('PCoA_plot.pdf', dpi = 300, height = 70, width = 100, units = ('mm'))

# PCoA_plot but with region
rownames(region_no_cent) <- region_no_cent$X.SampleID
region_no_cent <- region_no_cent[rownames(plot_frame), 'Region']

region_plot <- ggplot(plot_frame, aes(Axis.2, Axis.1, fill = region_no_cent, color = region_no_cent)) +
                geom_point(size=0.5) +
                stat_ellipse(show.legend = FALSE) +
                theme_bw() +
                # scale_color_manual(values = c('#B24D5E', '#4D5EB2')) +
                xlim(-0.55, 0.65) +
                ylim(-0.55, 0.65) +
                xlab(paste0("PCoA1 ",x_label,"%")) +
                ylab(paste0("PCoA2 ",y_label,"%")) +
                theme(axis.text = element_text(size = 10, color = 'black'),
                        panel.grid.major = element_blank(), 
                        panel.grid.minor = element_blank(),
                        panel.background = element_blank(),
                        # legend.position = c(1.5, 1.5),
                        legend.key.size = unit(0.5, 'cm'),
                        legend.title = element_blank(),
                        text = element_text(size = 10))
ggsave('region_pcoa_plot.pdf', dpi = 300, height = 70, width = 100, units = ('mm'))

pca <- prcomp(t(abundance_no_cent))
umap_frame <- data.frame(umap(t(abundance_no_cent))$layout)
# pca_frame <- data.frame(pca$x)[,1:2]
x_label<-round(pca$sdev[1]^2/sum(pca$sdev^2)*100,2)
y_label<-round(pca$sdev[2]^2/sum(pca$sdev^2)*100,2)
pca_frame$Env <- region_no_cent
umap_frame$Env <- region_no_cent
colnames(umap_frame) <- c('UMAP1', 'UMAP2', 'Env')

ggplot(umap_frame, aes(UMAP1, UMAP2, fill = Env, color = Env)) +
                geom_point(size=0.5) +
                stat_ellipse(show.legend = FALSE, level = 0.95) +
                theme_bw() +
                # scale_color_manual(values = c('#B24D5E', '#4D5EB2')) +
                # xlim(-0.55, 0.65) +
                # ylim(-0.55, 0.65) +
                theme(axis.text = element_text(size = 10, color = 'black'),
                        panel.grid.major = element_blank(), 
                        panel.grid.minor = element_blank(),
                        panel.background = element_blank(),
                        # legend.position = c(1.5, 1.5),
                        legend.key.size = unit(0.5, 'cm'),
                        legend.title = element_blank(),
                        text = element_text(size = 10))
ggsave('region_umap_plot.pdf', dpi = 300, height = 70, width = 100, units = ('mm'))

ggplot(pca_frame, aes(PC1, PC2, fill = Env, color = Env)) +
                geom_point(size=0.5) +
                stat_ellipse(show.legend = FALSE) +
                theme_bw() +
                # scale_color_manual(values = c('#B24D5E', '#4D5EB2')) +
                # xlim(-0.55, 0.65) +
                # ylim(-0.55, 0.65) +
                theme(axis.text = element_text(size = 10, color = 'black'),
                        panel.grid.major = element_blank(), 
                        panel.grid.minor = element_blank(),
                        panel.background = element_blank(),
                        # legend.position = c(1.5, 1.5),
                        legend.key.size = unit(0.5, 'cm'),
                        legend.title = element_blank(),
                        text = element_text(size = 10))
ggsave('region_pca_plot.png', dpi = 300, height = 70, width = 100, units = ('mm'))
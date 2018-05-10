#! /apps/r/3.1.1/bin/Rscript

library(ggplot2)

pdf(NULL)

nums <- read.csv("data/incompatibility_groups/blast_results/evalues.list", header=FALSE)
summary(nums)
str(nums)

ggplot(data=nums, aes(nums$V1)) + 
	geom_histogram(binwidth=0.1, col="cornflowerblue", fill="cornflowerblue") + 
	xlab("E Value") + 
	ylab("Frequency") + 
	ggtitle("Blast Results (identity >= 80%) E Values Histogram") + 
	theme_bw()

ggsave("data/incompatibility_groups/blast_results/evalues.pdf", height=10, width=10, units="in")

nums.cov60 <- read.csv("data/incompatibility_groups/blast_results/evalues_cov60.list", header=FALSE)
summary(nums.cov60)
str(nums.cov60)

ggplot(data=nums.cov60, aes(nums.cov60$V1)) + 
	geom_histogram(binwidth=0.00000000000000000000000001, col="cornflowerblue", fill="cornflowerblue") + 
	xlab("E Value") + 
	ylab("Frequency") + 
	ggtitle("Blast Results (identity >= 80%, subject_coverage >= 60%) E Values Histogram") + 
	theme_bw()

ggsave("data/incompatibility_groups/blast_results/evalues_cov60.pdf", height=10, width=10, units="in")

q()

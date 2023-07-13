library(dplyr)
my_data <- read.delim(file.choose())
head(my_data)
my_data$Isolate <- as.factor(my_data$Isolate)
levels(my_data$Isolate)
group_by(my_data, Isolate) %>%
summarise(count = n(),mean = mean(Severity, na.rm = TRUE),
sd = sd(Severity, na.rm = TRUE),
median = median(Severity, na.rm = TRUE),IQR = IQR(Severity, na.rm = TRUE))
kruskal.test(Severity ~ Isolate, data = my_data)
pairwise.wilcox.test(my_data$Severity, my_data$Isolate, p.adjust.method = "BH")


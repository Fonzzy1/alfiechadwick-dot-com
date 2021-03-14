# Title     : Week 2
# Objective : tute work for week 2
# Created by: fonzzy
# Created on: 9/3/21
library("readxl")
library("dplyr")

# 1) Collect data from other students in your class on how long it took them to get to University today, and how they got here; whether by car or motorbike [code 1], public transport [2] or by other means such as cycling or walking [3].
time <- c(30,20,45, 45,45, 35, 15, 20, 30, 60, 15, 60, 30, 50, 10, 40 )
code <- c(1,3,1,2,2,2,3,1,1,2,3,2,1,2,3,2)
df_1 <- data.frame(time, code)


#1 Manually, find the minimum, maximum, median and quartiles of the times taken to get to University, ie find the 5-number summary for the data.
summary(time)


#Manually construct a boxplot of the time data, including testing for any outliers.
boxplot(time, ylim = c(0,70))


#Use your scientific calculator (as allowed in the final exam) and Excel (investigate fx) to find the mean and standard deviation of the time data. Compare the values obtained for the mean and median.
mean(time)
sd(time)


#2.Open the excel file: “STA1010 Travel Times”, which contains a much larger (but similar) dataset
df_2 <- read_excel("./Excel files/STA1010 Travel Times-2009.xls",col_types = NULL, col_names = TRUE, skip = 1)

# Construct a frequency distribution (or histogram) of all the times taken to travel to Uni
hist(df_2$`Time taken (mins)`)


#The five-number summaries found for each mode of transport are given below
code1 <- df_2$`Time taken (mins)`[which(df_2$Code == 1)]
code2 <- df_2$`Time taken (mins)`[which(df_2$Code == 2)]
code3 <- df_2$`Time taken (mins)`[which(df_2$Code == 3)]

summary(code1)
summary(code2)
summary(code3)

 #Construct side-by side boxplots for travel times for the groups.
boxplot(code1, code2, code3)

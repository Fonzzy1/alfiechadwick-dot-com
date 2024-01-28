library(tidyverse)
library(xgdboost)

training_data <- readRDS("data/training_data.rds")
inferance <- readRDS("data/inferance.rds")


data_cols <- c(
  "weeks_with_more_than_7",
  "peak_week_JJJ",
  "peak_plays_JJJ",
  "first_play",
  "total_plays",
  "weeks_in_charts",
  "peak_in_charts",
  "chart_score"
)


train <- as.matrix(training_data[, data_cols])
train <- as.matrix(inferance[, data_cols])

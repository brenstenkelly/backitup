#fastscore.schema.0: rfinput
#fastscore.schema.1: rfoutput
#fastscore.recordsets.$all: true
#fastscore.module-attached: gbm
#fastscore.module-attached: readr
#fastscore.module-attached: lubridate
#fastscore.module-attached: tidyr

library(gbm)
library(readr)
library(lubridate)
library(tidyr)

begin <- function(){

  gbm1 <<- readRDS('gbm_example.rds')
  ls <- readRDS('medians.rds')
  columns <<- readRDS('columns.rds')
  character_vars <<- readRDS('character_vars.rds')
  best.iter <<- readRDS('best_iter.rds')
  medians <<- ls[1]
  modes <<- ls[2]
}

action <- function(x){
  replace_na(x, medians)
  replace_na(x, modes)
  x[, character_vars] <- lapply(x[, character_vars], as.factor)

  x <- as.data.frame(unclass(x))
  preds <- predict(gbm1, newdata=x[,columns], n.trees = best.iter, type = "link")
emit(data.frame("pred"= preds, "ID"=x$SK_ID_CURR))
}

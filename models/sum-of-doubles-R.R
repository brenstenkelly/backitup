# fastscore.schema.0: four-doubles
# fastscore.schema.1: double

action <- function(dat){
  the_sum <-  dat[[1]] + dat[[2]] + dat[[3]] + dat[[4]]
  emit(the_sum)
}

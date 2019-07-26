# fastscore.schema.0: double
# fastscore.schema.1: double

action <- function(datum){
    emit(datum + 1)
}

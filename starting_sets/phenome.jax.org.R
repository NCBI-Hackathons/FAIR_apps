
# read in jax.phenome.org data sets

setwd("~/Desktop/2019/2019BioITWorld")
studies      <- read.csv("studies.csv",header=TRUE, stringsAsFactors = FALSE)
measurements <- read.csv("measurements.csv",header=TRUE, stringsAsFactors=FALSE) 

measurements.df <- data.frame(measurements)

#install.packages("rjson")
library(rjson)

# 2019 April 12 ADM
# after downloading the json file with postman using the api
# GET Https://phenome.jax.org/api/pheno/strain/Chesler3
# then I downloaded the results
#
# had to remove the first line from the json file which gives the counts
#
Chesler3.json   <- fromJSON(file="Chesler3.strainmeans.response.json")

Chesler3.df <- lapply(Chesler3.json, function(play) # Loop through each "play"
{
  # Convert each group to a data frame.
  # This assumes you have 6 elements each time
  data.frame(matrix(unlist(play), ncol=13, byrow=T))
})

# Now you have a list of data frames, connect them together in
# one single dataframe
Chesler3.df <- do.call(rbind, Chesler3.df)

# Make column names nicer, remove row names
colnames(Chesler3.df) <- names(Chesler3.json[[1]][[1]])
rownames(Chesler3.df) <- NULL

chessler3.measures<-table(Chesler3.df$varname)
chessler3.measures.df = data.frame(chessler3.measures)
colnames(chessler3.measures.df) = c("name","count")
rownames(chessler3.measures.df) = as.character(names(chessler3.measures))

#
# merge the Chessler3.measures.df with the measurements.df by measnum
#
m <- merge(measurements.df, Chesler3.df, by="measnum")

#
# simple plot of the measurements 
library(ggplot2)
ggplot(data = measures.df, mapping = aes(x = name, y = count)) +
  geom_boxplot()


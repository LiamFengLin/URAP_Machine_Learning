rm(list=objects())

options(error=traceback)

library(tm)
library(SnowballC) # also needed for stemming function

a <- Corpus(DirSource("~/Desktop/URAP/text_analysis/data_2015_10_10/diff_poli_soc")) #the directory should have two text files in it, the files you want to compare
summary(a)

a <- tm_map(a, content_transformer(function(x) iconv(x, "latin1", "ASCII", sub = " ")), mc.cores=1)

a <- tm_map(a, content_transformer(tolower), mc.cores=1) # convert all text to lower case
a <- tm_map(a, content_transformer(removePunctuation), mc.cores=1) 
a <- tm_map(a, content_transformer(removeNumbers), mc.cores=1)
a <- tm_map(a, removeWords, stopwords("english"), mc.cores=1)

a <- tm_map(a, stemDocument, language = "english", mc.cores=1) # converts terms to tokens
a.dtm <- TermDocumentMatrix(a) #puts tokens into a term document matrix
a.dtm.sp <- removeSparseTerms(a.dtm, sparse=0.50) #remove sparse terms, the sparse number should be higher with a large number of documents, smaller with small number of documents, always less than 1
a.dtm.sp.df <- as.data.frame(inspect(a.dtm.sp)) # convert document term matrix to data frame
a.dtm.sp.df <- t(a.dtm.sp.df) #transpose matrix
rowTotals <- apply(a.dtm.sp.df, 1, sum) #create column with row totals, total number of words per document
head(rowTotals)
prop <- a.dtm.sp.df/rowTotals #change frequencies to proportions
prop <- t(prop)
head(prop)
data <- as.data.frame(prop)
data$diff <- data$PoliSciJobRumors.csv - data$SocJobRumors.csv #creates new column (diff) which is the difference between columns 1 and 2, need to change the names to fit your file names
sorted <- data[with(data,order(data$diff)),] #sorts data by column diff

first_rows <- cbind(row.names(sorted)[1:200], sorted[1:200,3]) #prints last row names
last_rows <- cbind(row.names(sorted)[(dim(sorted)[1] - 200):dim(sorted)[1]], sorted[(dim(sorted)[1] - 200):dim(sorted)[1],3]) #prints last row names, change the numbers to fit your matrix

write.csv(first_rows, file = "result_poli_soc/diffprop_soc_terms.csv") #writes csv file with the first rows and weights
write.csv(last_rows, file = "result_poli_soc/diffprop_poli_sci_terms.csv") #dito with the last rows

rm(list=objects())

a <- Corpus(DirSource("~/Desktop/URAP/text_analysis/data_2015_10_10/diff_poli_econ")) #the directory should have two text files in it, the files you want to compare
summary(a)

a <- tm_map(a, content_transformer(function(x) iconv(x, "latin1", "ASCII", sub = " ")), mc.cores=1)

a <- tm_map(a, content_transformer(tolower), mc.cores=1) # convert all text to lower case
a <- tm_map(a, content_transformer(removePunctuation), mc.cores=1) 
a <- tm_map(a, content_transformer(removeNumbers), mc.cores=1)
a <- tm_map(a, removeWords, stopwords("english"), mc.cores=1)

a <- tm_map(a, stemDocument, language = "english", mc.cores=1) # converts terms to tokens
a.dtm <- TermDocumentMatrix(a) #puts tokens into a term document matrix
a.dtm.sp <- removeSparseTerms(a.dtm, sparse=0.50) #remove sparse terms, the sparse number should be higher with a large number of documents, smaller with small number of documents, always less than 1
a.dtm.sp.df <- as.data.frame(inspect(a.dtm.sp)) # convert document term matrix to data frame
a.dtm.sp.df <- t(a.dtm.sp.df) #transpose matrix
rowTotals <- apply(a.dtm.sp.df, 1, sum) #create column with row totals, total number of words per document
head(rowTotals)
prop <- a.dtm.sp.df/rowTotals #change frequencies to proportions
prop <- t(prop)
head(prop)
data <- as.data.frame(prop)
data$diff <- data$EconJobRumors.csv - data$PoliSciJobRumors.csv #creates new column (diff) which is the difference between columns 1 and 2, need to change the names to fit your file names
sorted <- data[with(data,order(data$diff)),] #sorts data by column diff

first_rows <- cbind(row.names(sorted)[1:200], sorted[1:200,3]) #prints last row names
last_rows <- cbind(row.names(sorted)[(dim(sorted)[1] - 200):dim(sorted)[1]], sorted[(dim(sorted)[1] - 200):dim(sorted)[1],3]) #prints last row names, change the numbers to fit your matrix

write.csv(first_rows, file = "result_poli_econ/diffprop_poli_sci_terms.csv") #writes csv file with the first rows and weights
write.csv(last_rows, file = "result_poli_econ/diffprop_econ_terms.csv") #dito with the last rows

rm(list=objects())

a <- Corpus(DirSource("~/Desktop/URAP/text_analysis/data_2015_10_10/diff_soc_econ")) #the directory should have two text files in it, the files you want to compare
summary(a)

a <- tm_map(a, content_transformer(function(x) iconv(x, "latin1", "ASCII", sub = " ")), mc.cores=1)

a <- tm_map(a, content_transformer(tolower), mc.cores=1) # convert all text to lower case
a <- tm_map(a, content_transformer(removePunctuation), mc.cores=1) 
a <- tm_map(a, content_transformer(removeNumbers), mc.cores=1)
a <- tm_map(a, removeWords, stopwords("english"), mc.cores=1)

a <- tm_map(a, stemDocument, language = "english", mc.cores=1) # converts terms to tokens
a.dtm <- TermDocumentMatrix(a) #puts tokens into a term document matrix
a.dtm.sp <- removeSparseTerms(a.dtm, sparse=0.50) #remove sparse terms, the sparse number should be higher with a large number of documents, smaller with small number of documents, always less than 1
a.dtm.sp.df <- as.data.frame(inspect(a.dtm.sp)) # convert document term matrix to data frame
a.dtm.sp.df <- t(a.dtm.sp.df) #transpose matrix
rowTotals <- apply(a.dtm.sp.df, 1, sum) #create column with row totals, total number of words per document
head(rowTotals)
prop <- a.dtm.sp.df/rowTotals #change frequencies to proportions
prop <- t(prop)
head(prop)
data <- as.data.frame(prop)
data$diff <- data$SocJobRumors.csv - data$EconJobRumors.csv #creates new column (diff) which is the difference between columns 1 and 2, need to change the names to fit your file names
sorted <- data[with(data,order(data$diff)),] #sorts data by column diff

first_rows <- cbind(row.names(sorted)[1:200], sorted[1:200,3]) #prints last row names
last_rows <- cbind(row.names(sorted)[(dim(sorted)[1] - 200):dim(sorted)[1]], sorted[(dim(sorted)[1] - 200):dim(sorted)[1],3]) #prints last row names, change the numbers to fit your matrix

write.csv(first_rows, file = "result_soc_econ/diffprop_econ_terms.csv") #writes csv file with the first rows and weights
write.csv(last_rows, file = "result_soc_econ/diffprop_soc_terms.csv") #dito with the last rows


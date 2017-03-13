# PRIDE Cluster clusters all MS/MS spectra submitted to PRIDE Archive repository release: 2015-04
# http://www.ebi.ac.uk/pride/cluster/

# Description:The present script provides a reliable QC (Quality control) report about MGF files generated. 
# This script must be in the folder /nfs/nobackup/pride/cluster-prod/archive_spectra 


# Upload packages
packages <- c( "ggplot2", "scales", "knitr", "markdown", "tidyr", "rmarkdown","gridExtra", "stringr","data.table")
if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
    install.packages(setdiff(packages, rownames(installed.packages())))  }


library("ggplot2"); library("scales"); library("knitr"); library("markdown"); 
library("tidyr"); library("rmarkdown"); library("gridExtra"); library("stringr"); library("data.table")
 
### **Files**
#REPLACE RELEASE 2 WITH THE PATH OF THE NEW RELEASE
# release1_iden <- "/nfs/nobackup/pride/cluster-prod/archive_spectra/archive_identified_2016-10"
# release1_unid <- "/nfs/nobackup/pride/cluster-prod/archive_spectra/archive_unidentified_2016-10"
# 
# release2_iden <- "/nfs/nobackup/pride/cluster-prod/archive_spectra/archive_identified_2016-10"
# release2_unid <- "/nfs/nobackup/pride/cluster-prod/archive_spectra/archive_unidentified_2016-10"

release1_iden <- "~/Dropbox/Script_R_Cambridge/Script2/archive_identified_2016-10"
release1_unid <- "~/Dropbox/Script_R_Cambridge/Script2/archive_unidentified_2016-10"

release2_iden <- "~/Dropbox/Script_R_Cambridge/Script2/archive_identified_2016-10"
release2_unid <- "~/Dropbox/Script_R_Cambridge/Script2/archive_unidentified_2016-10"


#Count files how many files are in the folder. 
#Load files from last 
#file_all <- list.files(file.path(getwd(), "testall"), pattern = "\\.mgf$") 
file_iden <- list.files(file.path(getwd(), "archive_identified_2016-10"), pattern = "\\.mgf$") 
file_unide <- list.files(file.path(getwd(), "archive_unidentified_2016-10"), pattern = "\\.mgf$")

#NEW RELEASE. REPLACE WITH THE NEW FOLDER. 
file_iden2 <- list.files(file.path(getwd(), "archive_identified_2016-10"), pattern = "\\.mgf$") 
file_unide2 <- list.files(file.path(getwd(), "archive_unidentified_2016-10"), pattern = "\\.mgf$")

#Create a data frame with the data obtained: 
df.test <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(file_iden)+length(file_unide)), length(file_iden),length(file_unide)))

df.test2 <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(file_iden2)+length(file_unide2)), length(file_iden2),length(file_unide2)))

cat("\nNumber of files in Release 1")
kable(df.test, padding = 0)
cat("\nNumber of files in Release 2")
kable(df.test2, padding = 0)

df.id_and_uni <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(file_iden),length(file_unide)) )
df.id_and_uni2 <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(file_iden2),length(file_unide2)) )
 
#Create the pie chart

a <- ggplot(transform(transform(df.id_and_uni, Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2), 
            aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    ggtitle("Release 1") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

b <- ggplot(transform(transform(df.id_and_uni2, Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2), 
            aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    ggtitle("Release 2") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

grid.arrange(a, b, ncol=2)
 
#Number of files with data. 

setwd(release1_iden)
list_of_iden <- file.info(dir())
setwd(release1_unid)
list_of_unid <- file.info(dir())

setwd(release2_iden)
list_of_iden2 <- file.info(dir())
setwd(release2_unid)
list_of_unid2 <- file.info(dir())


# Get the size for each file

setwd(release1_iden)
size_iden <- file.info(dir(path = release1_iden))$size
setwd(release1_unid)
size_uniden <- file.info(dir(path = release1_unid))$size

setwd(release2_iden)
size_iden2 <- file.info(dir(path = release2_iden))$size
setwd(release1_unid)
size_uniden2 <- file.info(dir(path = release2_unid))$size



# subset the files that have non-zero size
iden_with_data <-  rownames(list_of_iden)[which(size_iden != 0)]
unid_with_data <-  rownames(list_of_unid)[which(size_uniden != 0)]

iden_with_data2 <-  rownames(list_of_iden2)[which(size_iden2 != 0)]
unid_with_data2 <-  rownames(list_of_unid2)[which(size_uniden2 != 0)]


# get the empty files
#all_without_data <-  rownames(list_of_all)[which(size_all == 0)]
iden_without_data <-  rownames(list_of_iden)[which(size_iden == 0)]
unid_without_data <-  rownames(list_of_unid)[which(size_uniden == 0)]

iden_without_data2 <-  rownames(list_of_iden2)[which(size_iden2 == 0)]
unid_without_data2 <-  rownames(list_of_unid2)[which(size_uniden2 == 0)]

 
### **With data**
#plot with data.

df_with_data_all <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(iden_with_data)+length(unid_with_data)),length(iden_with_data),length(unid_with_data)) )
cat("\nNumber of files with identify data")
kable(df_with_data_all, padding = 0)


df_with_data_all2 <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(iden_with_data2)+length(unid_with_data2)),length(iden_with_data2),length(unid_with_data2)) )
cat("\nNumber of files with unidentify data")
kable(df_with_data_all, padding = 0)


df_with_data <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(iden_with_data),length(unid_with_data)) )

df_with_data2 <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(iden_with_data2),length(unid_with_data2)) )

a <- ggplot(transform(transform(df_with_data , Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2),        aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

b <- ggplot(transform(transform(df_with_data2 , Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2),        aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

grid.arrange(a, b, ncol=2)
 

### **Without data**


#without data. 
df_without_data_all <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(iden_without_data)+length(unid_without_data)),length(iden_without_data),length(unid_without_data)) )
cat("\nNumber of files without identify data")
kable(df_without_data_all,padding = 0)

df_without_data_all2 <- data.frame(Types = c("Total", "Identify", "Unidentify"), Spectra= c((length(iden_without_data2)+length(unid_without_data2)),length(iden_without_data2),length(unid_without_data2)) )
cat("\nNumber of files without unidentify data")
kable(df_without_data_all2,padding = 0)


df_without_data <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(iden_without_data),length(unid_without_data)) )

df_without_data2 <- data.frame(Types = c("Identify", "Unidentify"), Spectra= c(length(iden_without_data2),length(unid_without_data2)) )


a <- ggplot(transform(transform(df_without_data , Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2), 
            aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

b <- ggplot(transform(transform(df_without_data2 , Spectra=Spectra/sum(Spectra)), labPos=cumsum(Spectra)-Spectra/2), 
            aes(x="", y = Spectra, fill = Types)) +
    geom_bar(width = 1, stat = "identity") +
    coord_polar(theta = "y") +
    geom_text(aes(y=labPos, label=scales::percent(Spectra)), size=7)

grid.arrange(a, b, ncol=2)

 

### **Modifications id**


setwd("~/Dropbox/Script_R_Cambridge/Script2/cache")
#setwd("/nfs/nobackup/pride/cluster-prod/archive_spectra/cache")
files_to_read <- file.info(dir())
size <- file.info(dir(path = "~/Dropbox/Script_R_Cambridge/Script2/cache"))$size
#size <- file.info(dir(path = "/nfs/nobackup/pride/cluster-prod/archive_spectra/cache"))$size
files_to_read <-  rownames(files_to_read)[which(size != 0)]

#Use the list a generate 
alldfs <- lapply(files_to_read, function(x) { 
    textfiles <- read.table(x, quote="\"", comment.char="")
})

alldfs <- lapply(x = alldfs, seq_along(alldfs), function(x, i) {
    assign(paste0(files_to_read[i]), x[[i]], envir=.GlobalEnv)
})
 



#MODIFICATIONS ONLY IN MODIFICATIONS_IDE.TXT
modifications <- data.frame(modifications=gsub("USER03=", "", modifications_ide.txt$V1))

modifications_2 <- data.frame(modifications=gsub("USER03=", "", modifications_ide.txt$V1))

#Split dataset. 
modifications2<- data.frame(str_split_fixed(modifications$modifications, ",", 20))


#If you want to check how many columns are empty, you can use the code below: 
#columns_emply <- histo2[!sapply(histo2, function(x) all(x == ""))]
#columns_emply <- histo2_2[!sapply(histo2_2, function(x) all(x == ""))]

#Merge the columns in one. 
modifications3 <- melt(setDT(modifications2),                              # set df to a data.table
                       measure.vars = list(c(1:20)),    # set column groupings
                       value.name = 'V')[                      # set output name scheme
                           , -1, with = F]


#Remove white rows.  
modifications3[modifications3==""] <- NA
modifications3 = subset(modifications3, V1 != " ")

#Remove first part of the string [num]-
modifications4 <- data.frame(modifications=gsub(" [A-Za-z] ", "", gsub("[0-9]*-", "", modifications3$V1)))

#Histograma: 
modifications5 <- data.frame(table(modifications4))
kable(modifications5, row.names = FALSE, padding = 0)


### **Sequences identified** 


sequences <- data.frame(sequences=gsub("SEQ=", "", sequences_ide.txt$V1))
sequences2 <- data.frame(table(sequences))
cat("\nThere are",nrow(sequences2), "sequences different.\n")
cat("The number of sequences is:", sum(sequences2$Freq))

 

### **Spectrum**



spectrum_ide <- data.frame(spectrum_ide=gsub("spectrum=", "", spectrum_ide.txt$V1))
#Remove strings in the column
spectrum_ide <- data.frame(spectrum_ide=spectrum_ide[grep("[[:digit:]]", spectrum_ide$spectrum_ide), ])

spectrum_unid <- data.frame(spectrum_unid=gsub("spectrum=", "", spectrum_unid.txt$V1))
#Remove strings in the column
spectrum_unid <- data.frame(spectrum_unid=spectrum_unid[grep("[[:digit:]]", spectrum_unid$spectrum_unid), ])


cat("\nThe number of spectrum identified:", sum(as.numeric(spectrum_ide$spectrum_ide)))
cat("\nThe number of spectrum unidentified:", sum(as.numeric(spectrum_unid$spectrum_unid)))

 

### **Taxonomy** 

taxonomy_ide <- data.frame(spectrum_ide=gsub("TAXONOMY=", "", taxonomy_ide.txt$V1))

taxonomy_unide <- data.frame(spectrum_ide=gsub("TAXONOMY=", "", taxonomy_unid.txt$V1))


taxonomy_ide <- data.frame(table(taxonomy_ide))
taxonomy_unide <- data.frame(table(taxonomy_unide))

kable(taxonomy_ide, row.names = FALSE, padding = 0)
kable(taxonomy_unide, row.names = FALSE, padding = 0)



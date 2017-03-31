#!/bin/sh

##### VARIABLES
# the name to give to the LSF job (to be extended with additional info)
JOB_NAME="QC_MGF_FILES"
# the job parameters that are going to be passed on to the job (build below)
JOB_PARAMETERS=""
# memory limit
MEMORY_LIMIT=40000
# LSF email notification
JOB_EMAIL="pride-report@ebi.ac.uk"
LOG_FILE_NAME="${JOB_NAME}"
VERSION="2015-04"
QUALITY="2"
OUTPUT_DIRECTORY="/nfs/pride/work/cluster/cluster-file-exporter/"


python ./Counter_files.py

Rscript -e "rmarkdown::render('QC_MGF_test.Rmd')"
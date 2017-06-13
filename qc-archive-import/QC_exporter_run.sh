#!/bin/sh

OUTPUT_DIRECTORY="/Users/yperez/"

python3.4 file_counter.py -i /Users/yperez/work/ms_work/cluster-work/archive_identified_2017-05 -o ${OUTPUT_DIRECTORY} -p /Users/yperez/work/ms_work/cluster-work/archive_identified_2015-05

Rscript -e "rmarkdown::render('QC_MGF_Report.Rmd', params=list(output='/Users/yperez/cache'))"
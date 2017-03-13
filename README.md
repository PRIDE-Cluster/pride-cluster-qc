# PRIDE CLUSTER QC

## QC for MGF files

The script for the QC of the MGF files ( Files obtained after the import of Data from PRIDE Archive) is in this repo in github().
This script Script_QC_MGF.Rmd  must be in the folder /nfs/nobackup/pride/cluster-prod/archive_spectra to be run. The path of the folder with the data generated from the current release should be changed inside the script.
The output file will be a html file with the following informations
   -  Number of files (Total, identified, unidentified) in both releases.
   -  Percent graph
   - Number of modifications
   - Total number of modifications and frequency.
   - Sequences identified in both releases.
   - Number of spectrum identified and unidentified
   - Taxonomy.

To generate the QC report,  run the script ./Script_QC_MGF.sh

## QC Clustering files

## QC for Spectrum libraries

## QC for Peptides Report

The script for the Peptides Report (.tsv files) is in this repo in github().

Information about: This pipeline generate a html file with the following information:

  - Repeated Sequences Results: This should be always 0.
  - Number of peptides and their increase or decrease.
  - Peptides with modifications, with non-modifications and their increase or decrease.
  - The sequences, modifications, projects, clusters and spectra of the new peptides in the current release.
  - A comparative modifications bar plot of the current version and the previous one.
  - The frequency of each modification.

To run the script QC_metrics_report.Rmd, this should be in the folder /nfs/pride/work/cluster.

   - To create the QC report you should change the path of the file that you are interesting to analyze.
   - Run the script ./QC_metrics_report.sh

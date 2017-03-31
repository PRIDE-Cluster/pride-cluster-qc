# PRIDE CLUSTER QC

## QC for MGF files

The script for the QC of the MGF files ( Files obtained after the import of Data from PRIDE Archive) is in this repo in github(https://github.com/PRIDE-Cluster/pride-cluster-qc/tree/master/QC_Export_MGF).
This QC is made by different script that must be runned orderly. Firstly: Counter_files.py and .Rmd. In order to facilitate this, a script has been created in bash that automatically executes these scripts.
These scripts must be in the folder /nfs/nobackup/pride/cluster-prod/archive_spectra to be run. The path of the folder with the data generated from the current release should be changed inside the scripts.
The output file will be a html file with the following informations
   -  Number of peptides in both releases (Identified, unidentified).
   -  Graphs that show the differences between both releases
   -  Number of modifications and new ones. 
   - Total number of modifications and frequency.
   - Number of identified and unidentified spectrum
   - Number of species in both releases
   - Number of spectrum identified and unidentified
   - Taxonomy.
   - Stacked barplot of the taxonomy.

To generate the QC report,  run the script ./QC_exporter_run.sh

## QC Clustering files

The python application to do a QC of the clustering files is: ./spectra-cluster-py-comparer-dev/spectra_cluster/ui/cluster_comparer_cli.py
To run this application you have to change the path of the total_clustering.file in "input" and choose a path for the output. 

./spectra-cluster-py-comparer-dev/spectra_cluster/ui/cluster_comparer_cli.py --input ./archive_clustering_all-2014-10/final.clustering,./archive_clustering_all-2014-10/final.clustering --output comparer.txt

#### IMPORTANT
The final_clustering file must be created by merging all files. This is done easily from the terminal and typing: 
  cat *.clustering > ./total.clustering

Sometimes, some spectra are repeated, which should not happen. If this happens, the duplicates must be deleted. For them there are two different applications written in perl and in python. My recommendation is to use Perl, since the execution time is shorter.
To run the perl script just type: 
    perl duplicate_remover.pl final.clustering.file


## QC for Spectrum libraries

## QC for Peptides Report

The script for the Peptides Report (.tsv files) is in this repo in github(https://github.com/PRIDE-Cluster/pride-cluster-qc/tree/master/QC_Peptide_Reports).

Information about: This pipeline generate a html file with the following information:

  - Repeated Sequences Results: This should be always 0.
  - Number of peptides and their increase or decrease.
  - Peptides with modifications, with non-modifications and their increase or decrease.
  - The sequences, modifications, projects, clusters and spectra of the new peptides in the current release.
  - A comparative modifications bar plot of the current version and the previous one.
  - The frequency of each modification.

To run the script QC_metrics_report.Rmd, this should be in the folder /nfs/pride/work/cluster.

   - To create the QC report you should change the path of the file that you are interesting to analyze.
   - Run the script ./reporterScript.sh


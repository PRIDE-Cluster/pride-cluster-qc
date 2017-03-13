#!/bin/bash

#Set working directory
WORKING_DIRECTORY1=`pwd`/cache
WORKING_DIRECTORY2=`pwd`/cache2

#Create a working directory for both releases
mkdir -p $WORKING_DIRECTORY1
mkdir -p $WORKING_DIRECTORY2

#Spliting data. 



# Go over the different files.
echo Working on files...


for path_to_hb_file in $( ls archive_identified_2016-10/*.mgf ); do
    echo $path_to_hb_file
    grep 'SEQ' $path_to_hb_file | cut -d "=" -f2- | tr ',' '\n' >> $WORKING_DIRECTORY/sequences_ide.txt
    grep 'TAXONOMY' $path_to_hb_file | cut -d "=" -f2- | tr ',' '\n' >> $WORKING_DIRECTORY/taxonomy_ide.txt
    grep 'USER' $path_to_hb_file | cut -d "=" -f2- >> $WORKING_DIRECTORY/modifications_ide.txt
    grep 'TITLE' $path_to_hb_file | sed 's/^.*\(spectrum.*\)/\1/g' | cut -d "=" -f2-  >> $WORKING_DIRECTORY/spectrum_ide.txt

done

for path_to_hb_file in $( ls archive_unidentified_2016-10/*.mgf ); do
    echo $path_to_hb_file
    grep 'SEQ' $path_to_hb_file | cut -d "=" -f2- | tr ',' '\n' >> $WORKING_DIRECTORY/sequences_unide.txt
    grep 'TAXONOMY' $path_to_hb_file | cut -d "=" -f2- | tr ',' '\n' >> $WORKING_DIRECTORY/taxonomy_unide.txt
    grep 'USER' $path_to_hb_file | cut -d "=" -f2- >> $WORKING_DIRECTORY/modifications_unide.txt
    grep 'TITLE' $path_to_hb_file | sed 's/^.*\(spectrum.*\)/\1/g' | cut -d "=" -f2-  >> $WORKING_DIRECTORY/spectrum_unide.txt

 done


#Para separar los archivos. 

awk '/^BEGIN IONS/{n++;w=1} n&&w{print > "out" n ".txt"} /^END IONS/{w=0}' PRD000001.mgf 







#Notas: 

#Coger los archivos MS
grep -n "MS:" ./modifications_ide.txt > MS_file.txt
#Elimianr los archivos MS
sed '/MS:/d' ./modifications_ide.txt > test1.txt


#Eliminar datos innecesarios y hacer el archivo leible. 
python -c 'import sys; print sys.stdin.read().replace(";", ",")' < test2.txt  > test3.txt


#Replace salto de línea por comas. 
python -c 'import sys; print sys.stdin.read().replace("\n", ",")' < test1.txt > test2.txt


#Remove the extra commas from the file: 

sed 's/,,*/,/g' test3.txt > test4.txt

#Eliminamos las comas por espacios
tr ',' '\n' < test4.txt  > test5.txt

#Remove first part. Position
sed  's/[0-9]*-//' test5.txt > test6.txt


sed '/MS:/d' ./modifications_ide.txt | python -c 'import sys; print sys.stdin.read().replace(";", ",")' | python -c 'import sys; print sys.stdin.read().replace("\n", ",")' | sed 's/,,*/,/g' | tr ',' '\n' | sed  's/[0-9]*-//' > prueba2.txt


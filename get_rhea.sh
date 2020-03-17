#!/bin/bash

# check arguments
if [[ $# -eq 0 ]];
then 
  echo "No folder name given"
  exit 1
fi 

# make directory based on argument name
mkdir -p $1 
cd $1

# download files and clean up 
curl -LOk https://github.com/Lagkouvardos/Rhea/archive/master.zip 
unzip master.zip
rm -f master.zip 

curl -LOk https://github.com/adamsorbie/bio_tools/blob/master/filter_otu_table.py 
curl -LOk https://raw.githubusercontent.com/adamsorbie/helper_scripts/master/import_phyloseq.R

mv filter_otu_table.py import_phyloseq.R Rhea-Master


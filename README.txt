# mc_cando_glioma provides the Python scripts and data files required to reproduce the results of our study


## System requirements 
All scripts have been tested on Windows 11 Version 10.0.26100 and Python version 3.12.8. Most modern computers and Python version 3 users should be able to run the scripts. 


## Installation
Download cando.py and the other Python scripts from the root folder of mc_cando_glioma, as well as the contents of the CANDO_data folder. Change the value of the variables cmpd_map, ind_map, and matrix_file in each script to match the location of your data files on your machine. Note that we used the approved compound list ‘drugbank-v2.9-approved.tsv’ and the matrix file ‘rd_ecfp4-int-dice-alphafold-homo_sapien-coach-c0.0-p0.0-CxP-approved.tsv’ for canbenchmark.py and the full compound list ‘drugbank-v2.9.tsv’ and the matrix file ‘filtered-alphafold-CxP-rd_ecfp4-v2.9-all.tsv’ for canpredict_compounds_and_top_targets.py         


## Usage
Benchmark CANDO by running canbenchmark.py. With the provided set of files, you should achieve the same figures that we provide in Benchmarking_Glioma.xlsx for AIA, IA, NAIA, NIA, ai-NDCG, NDCG indication, nNDCG all, and nNDCG indication.


To generate control values, use the script random_control.py to create a scrambled matrix based on our provided compound_proteome matrix. Then, run canbenchmark.py with the randomized control matrix swapped in as the matrix_file, and collect the figures. Repeat this 3 times programmatically and average the values for the control. Your figures will be slightly different, but not too different from the ones we provide in Benchmarking_Glioma.xlsx. 


To generate candidate drug predictions for treating glioma, run         canpredict_compounds_and_top_targets.py. This file will also generate top protein targets lists for our top 24 drug predictions. The process we used to narrow down our drug predictions list to 24 high corroboration candidates is described in our paper’s method section. 


## Installation and usage for overlap analyses


Download the overlap_analyses folder and run each Python script to generate the graphs and data files corresponding to Figures 4 and 5 in our paper. Each script is already linked to the appropriate data files. Alternatively, you can reproduce the figures using your own data by populating the Overlap_data folder according to the methodology described in the paper. 


The output file from summary.py contains the computed values used to generate the overlap percentage and Jaccard coefficient graphs.


## Open source license

This project is made available under the following terms:

Code is licensed under the MIT License. You are free to use, modify, and distribute the code with appropriate attribution.

Data is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0). You may share and adapt the data for any purpose, including commercial use, provided that proper credit is given.
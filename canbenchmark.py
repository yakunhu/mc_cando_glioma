import sys, os
import cando as cnd

cnd.get_data(v='v2.5', org='homo_sapien')
matrix_file = '/projects/academic/rams/sumeixu/rd_ecfp4-int-dice-alphafold-homo_sapien-coach-c0.0-p0.0-CxP-approved.tsv'
cmpd_map='/user/sumeixu/ondemand/data/sys/myjobs/projects/default/4/drugbank-v2.9-approved.tsv'
ind_map='/user/sumeixu/ondemand/data/sys/myjobs/projects/default/4/drugbank2ctd-v2.9.tsv'
protein_set = "tutorial-bac-prots.txt"
dist_metric = 'cosine'
ncpus = 6

cando = cnd.CANDO(cmpd_map, ind_map, matrix=matrix_file, compound_set='approved', compute_distance=True,
                  dist_metric=dist_metric, ncpus=ncpus) 

cando.canbenchmark (
file_name = 'summary.tsv',
continuous = False,
bottom = False,
ranking = 'standard',
adrs = False )

cando.canbenchmark_ndcg (
file_name = 'summary_ndcg.tsv' )

cando.canbenchmark_new (
file_name = 'summary2.tsv',
continuous = False,
bottom = False,
ranking = 'standard',
adrs = False )


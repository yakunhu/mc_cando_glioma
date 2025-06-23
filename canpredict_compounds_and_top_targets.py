import sys, os
import cando as cnd

cnd.get_data(v='v2.5', org='homo_sapien')
matrix_file = '/user/sumeixu/ondemand/data/sys/myjobs/projects/default/4/filtered-alphafold-CxP-rd_ecfp4-v2.9-all.tsv'
cmpd_map='/user/sumeixu/ondemand/data/sys/myjobs/projects/default/4/drugbank-v2.9.tsv'
ind_map='/user/sumeixu/ondemand/data/sys/myjobs/projects/default/4/drugbank2ctd-v2.9.tsv'
protein_set = "tutorial-bac-prots.txt"
dist_metric = 'cosine'
ncpus = 6

cando = cnd.CANDO(cmpd_map, ind_map, matrix=matrix_file, compound_set='all', compute_distance=True,
                  dist_metric=dist_metric, ncpus=ncpus) 

cando.canpredict_compounds(
 'MESH:D005910',
 n = 100,
 topX = 100,
 consensus = False,
 keep_associated = False,
 cmpd_set = 'full'
 save = 'compounds100.tsv' )
 
compound_ids = [42, 49, 64, 5106, 11200, 12744, 9584, 7874, 253, 54, 901, 2036, 3654, 454, 3331, 4645, 714, 9942, 5063, 7897, 4948, 11635, 10660, 10658]
for i, cmpb in enumerate(compound_ids, start=1):
    cando.top_targets(
        cmpb,
        n=100,
        negative=False,
        save_file=f'top_targets{i}'
    )


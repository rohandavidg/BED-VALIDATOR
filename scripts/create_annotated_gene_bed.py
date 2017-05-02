#!/dlmp/sandbox/cgslIS/rohan/Python-2.7.11/python

"""
This script validates only if an exon is listed in the
bed file
"""

import os
import argparse
import csv
import create_composite_bed
import subprocess

outdir = os.getcwd()
intersect_bed = '/usr/local/biotools/bedtools/2.20.1/bin/intersectBed'


def main(bed2):
    args = parse_args()
    run(bed2, args.bed_file)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-B', dest='bed_file',  required=True,
                        help='bed file to asses')
    args = parser.parse_args()
    return args

def run(bed2, bed_file):
    remove_gene_dir()
    annotate_bed_path = annotate_bed_file(bed_file, bed2)


def annotate_bed_file(bed_file, bed2):
#    bed_genes = set()
    gene_bed_list = []
    cmd = intersect_bed + ' -a ' + bed_file + ' -b ' + bed2 + ' -wa ' + ' -wb '
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out, err = p.communicate()
    for something in out.split('\n'):
        value = something.strip().split('\t')
        chrom = value[0]
        start = value[1]
        stop = value[2]
        gene = value[6]
#        bed_genes.add(gene)
        transcript = value[7]
        exon = value[8]
        gene_dir = make_gene_dir(gene)
        gene_bed = gene_dir + '/' + gene + '.bed'
        gene_bed_list.append(gene_bed)
        with open(gene_bed, 'a+') as fout:
            if exon.startswith('Ex'):
                fout.write(chrom + '\t' + str(start) + '\t' + str(stop) + '\t' + gene + '\t' + transcript + '\t' + exon + '\n')
            else:
                fout.write(chrom + '\t' + str(start) + '\t' + str(stop) + '\t' + gene + '\t' + transcript + '\t' + 'Ex' + exon + '\n')
    return gene_bed_list 


def make_gene_dir(gene):
    gene_dir = outdir + "/VALIDATION/" + gene
    if os.path.isdir(gene_dir):
        pass
    else:
        os.makedirs(gene_dir)
    return gene_dir


def remove_gene_dir():
    validation_dir = outdir + "/VALIDATION"
    if os.path.isdir(validation_dir):
        shutil.rmtree(validation_dir)
    else:
        pass
    


if __name__  == "__main__":
    composite_bed = create_composite_bed.main()    
    assert os.path.isfile('CGSL_composite.bed')
    main('CGSL_composite.bed')

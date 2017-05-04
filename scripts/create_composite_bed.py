#!/dlmp/sandbox/cgslIS/rohan/Python-2.7.11/python

"""
this script creates a composite bed file
"""

import os
import argparse
import csv
import gzip
import pprint
import sys
from GetRefFlat import GetRefFlat
import subprocess
import shlex

gtf_file = "/dlmp/sandbox/cgslIS/rohan/cgsl_code/bin/BED-VALIDATOR/files/Homo_sapiens.GRCh37.75.gtf.gz"
outdir = os.getcwd()

def main():
    transcipt_cds_dict = run()
    return transcipt_cds_dict

def run():
    ensemble_bed = outdir + "/ENSEMBL_cds_only.bed"
    refflat_final = outdir + "/FinalRefFlat.bed"
    composite_bed = outdir + "/CGSL_composite.bed"    
    if os.path.isfile(ensemble_bed):
        pass
    else:
        parsed_gtf_file = parse_gtf(gtf_file, ensemble_bed)

    if os.path.isfile(refflat_final):
        os.remove(refflat_final)
        parse_refflat_file = GetRefFlat(outdir)
        os.remove('refFlat.bed')
        create_composite_bed(composite_bed, ensemble_bed, refflat_final)
        transcipt_cds_file = write_out_cds(parse_refflat_file)
    else:
        parse_refflat_file = GetRefFlat(outdir)
        os.remove('refFlat.bed')
        create_composite_bed(composite_bed, ensemble_bed, refflat_final)
        transcipt_cds_file = write_out_cds(parse_refflat_file)


def create_composite_bed(composite_bed_path, file1, file2):
    if os.path.isfile(composite_bed_path):
        os.remove(composite_bed_path)
        cat_files(composite_bed_path, file1, file2)
    else:
        cat_files(composite_bed_path, file1, file2)
    

def parse_gtf(gtf_file, outfile):
    with gzip.open(gtf_file) as csvfile, open(outfile, 'w') as fout:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            try:
                if row[2] == 'CDS':
                    chrom = 'chr' + row[0]
                    start = row[3]
                    stop = row[4]
                    transcript_id = row[8].split(';')[1]
                    exon_number = row[8].split(';')[2]
                    exon = shlex.split(exon_number.split(" ")[2])[0]
                    gene_name = row[8].split(';')[3]
                    strand = row[6]
                    gene = shlex.split(gene_name.split(" ")[2])[0]
                    transcript = shlex.split(transcript_id.split(" ")[2])[0]
                    out = (chrom, start, stop, gene, transcript, 'Ex' + exon, strand)
                    fout.write('\t'.join(str(i) for i in out) + '\n')
                else:
                    pass
            except IndexError:
                pass

def cat_files(bed_path, file1, file2):
    assert os.path.isfile(file1)
    assert os.path.isfile(file2)
    with open(bed_path, 'w+') as fout:
        for f in [file1, file2]:
            with open(f, 'r') as fin:
                for raw_line in fin:
                    value = raw_line.strip()
                    if value:
                        if "CHROM" in value:
                            pass
                        else:
                            fout.write(value + '\n')


def write_out_cds(transcript_dict):
    with open('Refeseq_transcipt_cds.tsv', 'w') as fout:
        for k, v in transcript_dict.items():
            fout.write(k +'\t' + v[0] + '\t' + v[1] + '\n')
            
                                              

if __name__ == "__main__":
    main()

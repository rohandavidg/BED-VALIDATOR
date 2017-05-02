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
sys.path.append("/dlmp/sandbox/cgslIS/Jag/WESTA/")
from GetRefFlat import GetRefFlat
import subprocess
import shlex

gtf_file = "/dlmp/sandbox/reference/ENSEMBL/build75/Homo_sapiens.GRCh37.75.gtf.gz"
refflat_file = "/dlmp/sandbox/reference/UCSC/refFlat"
outdir = os.getcwd()

def main():
    run()


def run():
    ensemble_bed = 'ENSEMBL_cds_only.bed'
    if os.path.isfile(ensemble_bed):
        pass
    else:
        parsed_gtf_file = parse_gtf(gtf_file, ensemble_bed)
    refflat_final = 'FinalRefFlat.bed'
    if os.path.isfile(refflat_final):
        os.remove(refflat_final)
        parse_refflat_file = GetRefFlat(outdir)
        os.remove('refFlat.bed')
    else:
        parse_refflat_file = GetRefFlat(outdir)
        os.remove('refFlat.bed')
    if os.path.isfile('CGSL_composite.bed'):
        os.remove('CGSL_composite.bed')
        create_composite_bed = cat_files(ensemble_bed, refflat_final)
    else:
        create_composite_bed = cat_files(ensemble_bed, refflat_final)

def parse_gtf(gtf_file, outfile):
    with gzip.open(gtf_file) as csvfile, open(outfile, 'w') as fout:
        reader = csv.reader(csvfile, delimiter='\t')
        print  reader
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

def cat_files(file1, file2):
    assert os.path.isfile(file1)
    assert os.path.isfile(file2)
    with open('CGSL_composite.bed', 'w+') as fout:
        for f in [file1, file2]:
            with open(f, 'r') as fin:
                for raw_line in fin:
                    value = raw_line.strip()
                    if value:
                        if "CHROM" in value:
                            pass
                        else:
                            fout.write(value + '\n')


if __name__ == "__main__":
    main()

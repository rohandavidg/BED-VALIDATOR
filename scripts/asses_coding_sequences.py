#!/dlmp/sandbox/cgslIS/rohan/Python-2.7.11/python

"""
coding sequeces to be assesed with transcript in
composite bed
"""

import os
import argparse
import csv
import subprocess
import logging
import time
import datetime
from collections import defaultdict
import create_composite_bed

TMP_OUT_DIR=os.getcwd()
logger_file = "bed_validation"


def main(transcript_cds_dict):
    args = parse_args()
    run(args.bed_file, args.composite_bed, transcript_cds_dict)


def run(bed_file, composite_bed, transcript_cds_dict):
    logger = configure_logger(logger_file)
    index_dict = index_composite_bed(composite_bed)
    compare_coding = asses_region(bed_file, index_dict, transcript_cds_dict, logger)
    

def parse_args():
    parser =  argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-b', dest='bed_file', type=argparse.FileType('r'),
                        help="path to gene bed file", required=True)
    parser.add_argument('-c', dest='composite_bed', type=argparse.FileType('r'),
                        help="path to composite bed file", required=True)
    args = parser.parse_args()
    return args


def configure_logger(filename):
    """
    setting up logging
    """
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(time.strftime(filename + "-%Y%m%d.log"))
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s'\t'%(name)s'\t'%(levelname)s'\t'%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



class bed_file():

    def __init__(self, line):
        value = line.split('\t')
        self.chrom = value[0].strip()
        self.start = int(value[1])
        self.stop = int(value[2])
        self.gene = value[3].strip()
        self.transcript = value[4].strip()
        self.exon =  value[5].strip()
        self.strand =  value[6].strip()

    def __iter__(self):
        return self

    def chromosome(self):
        return self.chrom

    def bed_start(self):
        return self.start
    
    def bed_stop(self):
        return self.stop

    def bed_gene(self):
        return self.gene

    def bed_transcript(self):
        return self.transcript


    def bed_exon(self):
        if not self.exon.startswith('Ex'):
            return 'Ex' + self.exon
        else:
            return self.exon

    def bed_strand(self):
        return self.strand


def index_composite_bed(composite_bed):
    index_composite_dict = {}
    headers = ['chrom', 'start', 'stop', 'gene', 'transcript', 'exon', 'strand']
    reader = csv.DictReader(composite_bed, delimiter='\t', fieldnames=headers)
    for row in reader:
        trascript = row['transcript']
        exon = row['exon']
        strand = row['strand']
        key = trascript + ':' + exon
        value = [row['start'], row['stop']]
        index_composite_dict[key] = value
    return index_composite_dict


def asses_region(gene_bed, index_composite_dict, transcript_cds_dict, logger):
    for raw_line in gene_bed:
        value = raw_line.strip()
        parse_bed = bed_file(value)
        chrom = parse_bed.chromosome()
        transcript = parse_bed.bed_transcript()
        start = parse_bed.bed_start()
        stop = parse_bed.bed_stop()
        exon = parse_bed.bed_exon()
        gene = parse_bed.bed_gene()
        strand = parse_bed.bed_strand()
        gene_key = transcript + ':' + exon 
        if index_composite_dict[gene_key]:
            check_position = compare_region(start, stop, index_composite_dict[gene_key][0], 
                                            index_composite_dict[gene_key][1], gene, transcript, exon, strand, transcript_cds_dict, logger)
                                            
    

def compare_region(gene_cds_start, gene_cds_stop, trans_cds_start, trans_cds_stop, gene, transcript, exon, strand, transcript_cds_dict, logger):
    if strand == '+':
        if int(gene_cds_start) <= int(trans_cds_start) <= int(gene_cds_stop):
            pass
        else:
            if transcript.startswith('NM_'):
                cds_start = int(transcript_cds_dict[transcript][0])
                cds_stop =  int(transcript_cds_dict[transcript][1])
                if cds_start <= int(gene_cds_start) <= cds_stop:
                    logger.debug("start {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_start, gene,
                                                                                                                        exon,
                                                                                                                        trans_cds_start,
                                                                                                                        transcript))
 
            else:
                logger.debug("start {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_start, gene, 
                                                                                                                exon,
                                                                                                                trans_cds_start, 
                                                                                                                transcript))
        if int(gene_cds_stop) >= int(trans_cds_stop):
            pass
        else:
            if transcript.startswith("NM_"):
                cds_start = int(transcript_cds_dict[transcript][0])
                cds_stop =  int(transcript_cds_dict[transcript][1])
                if cds_start <= int(gene_cds_stop) <=  cds_stop:
                    logger.debug("stop {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_stop, gene,
                                                                                                                        exon,
                                                                                                                        trans_cds_stop,
                                                                                                                        transcript))
            else:
                logger.debug("stop {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_stop, gene,
                                                                                                                   exon,
                                                                                                                   trans_cds_stop,
                                                                                                                   transcript))
    else:
        if int(gene_cds_start) <= int(trans_cds_start) <= int(gene_cds_stop):
            pass
        else:
            if transcript.startswith("NM_"):
                cds_start = int(transcript_cds_dict[transcript][0])
                cds_stop =  int(transcript_cds_dict[transcript][1])
                if cds_start <= int(gene_cds_start) <= cds_stop:
                    logger.debug("start {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_start, gene,
                                                                                                                        exon,
                                                                                                                        trans_cds_start,
                                                                                                                        transcript))
            else:
                logger.debug("start {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_start, gene,
                                                                                                                    exon,
                                                                                                                    trans_cds_start,
                                                                                                                    transcript))
        if int(gene_cds_stop) >= int(trans_cds_stop):
            pass
        else:
            if transcript.startswith("NM_"):
                cds_start = int(transcript_cds_dict[transcript][0])
                cds_stop =  int(transcript_cds_dict[transcript][1])
                print cds_start
                print int(gene_cds_stop)
                print cds_stop
                if cds_start <= int(gene_cds_stop) <= cds_stop:
                    logger.debug("stop {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_stop, gene,
                                                                                                                        exon,
                                                                                                                        trans_cds_stop,
                                                                                                                        transcript))
            else:
                logger.debug("stop {0} for gene {1} for exon {2} should be {3} according to transcript {4}".format(gene_cds_stop, gene,
                                                                                                                   exon,
                                                                                                                   trans_cds_stop,
                                                                                                                   transcript))


if __name__ == "__main__":
    transcript_cds_dict = create_composite_bed.main()
    main(transcript_cds_dict)


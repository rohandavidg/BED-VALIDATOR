#/usr/bin/python

import subprocess
import os 


def main(output_dir):
	transcript_cds_dict = GetRefFlat(output_dir)
	

def GetRefFlat(output_dir):
	Command = 'mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e "select chrom,txStart,txEnd,name,name2,exonStarts,exonEnds,strand,cdsStart,cdsEnd from refGene;" > ' + output_dir+ "/refFlat.bed"
	subprocess.call([Command], shell=True)
	ReflatBed = open(output_dir+ "/refFlat.bed","r")
	TmpCount = 0
	FinalRefFlat = open(output_dir + "/FinalRefFlat.bed","w")
	transcript_cds = {}
	for eachLine in ReflatBed:
		TmpCount += 1
		if TmpCount == 1:
			continue
		eachLine_Split = eachLine.split()
		GeneName = eachLine_Split[4]
		Tr = eachLine_Split[3]
		TrStarts = eachLine_Split[5].split(",")
		TrEnds = eachLine_Split[6].split(",")
		Chromosome = eachLine_Split[0]
		Strand = eachLine_Split[-3]
		CdsEnd = eachLine_Split[-1]
		CdsStart = eachLine_Split[-2]
		transcript_cds[Tr] = [CdsStart, CdsEnd]
		TrCount=0
		if Tr.startswith('NM_'):
			for eachStart in TrStarts:
				if len(eachStart)<1:
					continue
				#if int(eachStart) < int(CdsStart):
				#	continue
				FinalRefFlat.write(Chromosome+"\t"+eachStart+"\t"+TrEnds[TrCount]+"\t"+GeneName+ "\t" + Tr + "\t" + "Ex"+str(TrCount + 1) + "\t" + Strand + "\n")
				TrCount += 1
	FinalRefFlat.close()
	return transcript_cds


if __name__== "__main__":
	output_dir = os.getcwd()
	main(output_dir)

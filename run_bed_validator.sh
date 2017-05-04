#!/bin/bash
#set -o pipefail

usage ()
{
cat <<EOF
##########################################################################################################
##
## Script Options:
##   Required:
##      -c      config file
##
#########################################################################################################

EOF
}

##################################################################################
###
###     Parse Argument variables
###
##################################################################################


while getopts "c:" OPTION; do
    case $OPTION in
	c) CONFIG_FILE=$OPTARG ;;
	\?) echo "Invalid option: -$OPTARG. See output file for usage." >&2
            usage
            exit ;;
	:)  echo "Option -$OPTARG requires an argument. See output file for usage." >&2
            usage
            exit ;;
    esac
done


if [ -z $CONFIG_FILE ];then
    usage
    echo "config file parameter is missing"
    exit 1
else
    true
fi

BASE_DIR="$( dirname "$0" )"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $SCRIPT_DIR
source $CONFIG_FILE


logError(){
    local LEVEL="${1}"
    local CODE="${2}"
    local MESSAGE="${3}"
    >&2 echo "[$(date +%Y-%m-%d'T'%H:%M:%S%z) [${LEVEL}] [${SCRIPT_NAME}] [${JOB_ID-NA}] [${CODE}] ${MESSAGE}"
}

log(){
    local LEVEL="${1}"
    local CODE="${2}"
    local MESSAGE="${3}"
    echo "[$(date +%Y-%m-%d'T'%H:%M:%S%z) [${LEVEL}] [${SCRIPT_NAME}] [${JOB_ID-NA}] [${CODE}] ${MESSAGE}"
}


function check_variable() {
    message=$1
    if [[ "$2" == "" ]]
    then
        echo -e "\n************************************"
        echo "$message is not set correctly."
        logError "DEBUG" "-" "$message parameter missing in tool info"
        echo -e "\n************************************"
        exit 1;
    fi
}

check_variable "CONFIG_FILE:OUTPUT_DIRECTORY" $OUTPUT_DIRECTORY
check_variable "CONFIG_FILE:SGE" $SGE
check_variable "CONFIG_FILE:QUEUE" $QUEUE
check_variable "CONFIG_FILE:EMAIL" $EMAIL
check_variable "CONFIG_FILE:h_vmem" $h_vmem
check_variable "CONFIG_FILE:h_stack" $h_stack
check_variable "CONFIG_FILE:PYTHON" $PYTHON

COMPOSIT_BED=$OUTPUT_DIRECTORY/CGSL_composite.bed
VALIDATION_DIR=$OUTPUT_DIRECTORY/VALIDATION/
ASSES_BED=$SCRIPT_DIR/scripts/asses_coding_sequences.py
REFSEQ_MAPPING=$OUTPUT_DIRECTORY/Refeseq_transcipt_cds.tsv
bed_file=$(find "$VALIDATION_DIR" -name "*.bed")
for gene_bed in $bed_file;do
    base_dir=$(dirname $gene_bed)
    base=$(basename $gene_bed)
    pushd $base_dir > /dev/null
    if [ -d $base_dir/logs ];then
	mkdir $base_dir/logs
    else
	true
    fi
    sleep 1s
    gene=`echo $base_dir | rev | cut -d"/" -f1 | rev`
    only_gene_bed=$base_dir/$gene.bed
    echo $SGE -M $EMAIL -m a -l h_vmem=$h_vmem -l h_stack=$h_stack -b y -V -N validate_$gene -q $QUEUE -wd $base_dir -o $base_dir/logs -e $base_dir/logs $PYTHON $ASSES_BED -b $only_gene_bed -c $COMPOSIT_BED -t $REFSEQ_MAPPING
    $SGE -M $EMAIL -m a -l h_vmem=$h_vmem -l h_stack=$h_stack -b y -V -N validate_$base -q $QUEUE -wd $base_dir -o $base_dir/logs -e $base_dir/logs $PYTHON $ASSES_BE\
D -b $only_gene_bed -c $COMPOSIT_BED -t $REFSEQ_MAPPING
    popd > /dev/null
done


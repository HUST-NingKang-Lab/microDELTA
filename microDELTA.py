import argparse
import os

argparser = argparse.ArgumentParser(description = 'microDELTA: a tool for tracing tracing longitudinal changes in the human gut microbiome')
argparser.add_argument('-O', '--overall', help = 'Overall status of the hosts in csv format',
                       default = 'microbiomes.txt')
argparser.add_argument('-l', '--label', help = 'Label of the hosts in csv format',
                       default = 'experiments_repeat/exp_1/SourceMapper.csv')
argparser.add_argument('-o', '--output', help = 'Directory to store the intermediate files',
                       default = 'experiments_repeat/exp_1')
argparser.add_argument('-S', '--source', help = 'Abundance of training samples in tsv format',
                       default = 'experiments_repeat/exp_1/SourceCM.tsv')
argparser.add_argument('-Q', '--query', help = 'Abundance of testing samples in tsv format',
                       default = 'experiments_repeat/exp_1/QueryCM.tsv')
argparser.add_argument('-m', '--model', help = 'Base model directory. If not specified, an independent model will be trained',
                      default = '../aging/mst/model/disease_model')

args = argparser.parse_args()

os.system(f'expert construct -i {args.overall} -o {args.output}/ontology.pkl')
os.system(f'ls {args.source} > tmp; expert convert -i tmp --in-cm -o {args.output}/SourceCM.h5')
os.system(f'ls {args.query} > tmp; expert convert -i tmp --in-cm -o {args.output}/QueryCM.h5')

os.system(f'expert map --to-otlg -t {args.output}/ontology.pkl -i {args.label} -o {args.output}/SourceLabels.h5')
os.system(f'expert map --to-otlg -t {args.output}/ontology.pkl -i {args.label} -o {args.output}/QueryLabels.h5')

if args.model:
    os.system(f'expert transfer -i {args.output}/SourceCM.h5 -t {args.output}/ontology.pkl \
        -l {args.output}/SourceLabels.h5 -o {args.output}/Transfer_DM \
        -m {args.model} --finetune --update-statistics')
    os.system(f'expert search -i {args.output}/QueryCM.h5 -m {args.output}/Transfer_DM -o {args.output}/Search_Transfer_DM')
else:
    os.system(f'expert train -i {args.output}/SourceCM.h5 -t {args.output}/ontology.pkl \
        -l {args.output}/SourceLabels.h5 -o {args.output}/NN')
    os.system(f'expert search -i {args.output}/QueryCM.h5 -m {args.output}/NN -o {args.output}/Search_NN')
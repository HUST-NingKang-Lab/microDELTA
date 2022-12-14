expert construct -i microbiomes.txt -o ontology.pkl
for i in {1,2,3,4,5,6,7,8,9,10}; do
ls experiments_repeat/exp_$i/SourceCM.tsv > tmp; expert convert -i tmp --in-cm -o experiments_repeat/exp_$i/SourceCM.h5;
ls experiments_repeat/exp_$i/QueryCM.tsv > tmp; expert convert -i tmp --in-cm -o experiments_repeat/exp_$i/QueryCM.h5;

expert map --to-otlg -t ontology.pkl -i experiments_repeat/exp_$i/SourceMapper.csv -o experiments_repeat/exp_$i/SourceLabels.h5;
expert map --to-otlg -t ontology.pkl -i experiments_repeat/exp_$i/QueryMapper.csv -o experiments_repeat/exp_$i/QueryLabels.h5;

expert transfer -i experiments_repeat/exp_$i/SourceCM.h5 -t ontology.pkl \
        -l experiments_repeat/exp_$i/SourceLabels.h5 -o experiments_repeat/exp_$i/Transfer_DM \
        -m ../aging/mst/model/disease_model --finetune --update-statistics;
expert search -i experiments_repeat/exp_$i/QueryCM.h5 -m experiments_repeat/exp_$i/Transfer_DM -o experiments_repeat/exp_$i/Search_Transfer_DM;
expert evaluate -i experiments_repeat/exp_$i/Search_Transfer_DM -l experiments_repeat/exp_$i/QueryLabels.h5 -o experiments_repeat/exp_$i/Eval_Transfer_DM -S 0;
done
rm tmp
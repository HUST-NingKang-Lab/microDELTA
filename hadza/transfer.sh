expert construct -i microbiomes.txt -o ontology.pkl
for i in {0,1,2,3,4,5,6,7}; do
ls experiments/exp_$i/SourceCM.tsv > tmp; expert convert -i tmp --in-cm -o experiments/exp_$i/SourceCM.h5;
ls experiments/exp_$i/QueryCM.tsv > tmp; expert convert -i tmp --in-cm -o experiments/exp_$i/QueryCM.h5;

expert map --to-otlg -t ontology.pkl -i experiments/exp_$i/SourceMapper.csv -o experiments/exp_$i/SourceLabels.h5;
expert map --to-otlg -t ontology.pkl -i experiments/exp_$i/QueryMapper.csv -o experiments/exp_$i/QueryLabels.h5;

expert transfer -i experiments/exp_$i/SourceCM.h5 -t ontology.pkl \
        -l experiments/exp_$i/SourceLabels.h5 -o experiments/exp_$i/Transfer_DM \
        -m ../../Longevity_research/mst/model/disease_model --finetune --update-statistics;
expert search -i experiments/exp_$i/QueryCM.h5 -m experiments/exp_$i/Transfer_DM -o experiments/exp_$i/Search_Transfer_DM;
expert evaluate -i experiments/exp_$i/Search_Transfer_DM -l experiments/exp_$i/QueryLabels.h5 -o experiments/exp_$i/Eval_Transfer_DM -S 0;
done
rm tmp
expert construct -i microbiomes.txt -o ontology.pkl

for i in {0,1,2,3,4,5,6,7}; do
ls nn_result/exp_$i/SourceCM.tsv > tmp; expert convert -i tmp --in-cm -o nn_result/exp_$i/SourceCM.h5;
ls nn_result/exp_$i/QueryCM.tsv > tmp; expert convert -i tmp --in-cm -o nn_result/exp_$i/QueryCM.h5;

expert map --to-otlg -t ontology.pkl -i nn_result/exp_$i/SourceMapper.csv -o nn_result/exp_$i/SourceLabels.h5;
expert map --to-otlg -t ontology.pkl -i nn_result/exp_$i/QueryMapper.csv -o nn_result/exp_$i/QueryLabels.h5;

expert train -i nn_result/exp_$i/SourceCM.h5 -t ontology.pkl \
        -l nn_result/exp_$i/SourceLabels.h5 -o nn_result/exp_$i/NN
expert search -i nn_result/exp_$i/QueryCM.h5 -m nn_result/exp_$i/NN -o nn_result/exp_$i/Search;
expert evaluate -i nn_result/exp_$i/Search -l nn_result/exp_$i/QueryLabels.h5 -o nn_result/exp_$i/Eval -S 0;
done

rm tmp
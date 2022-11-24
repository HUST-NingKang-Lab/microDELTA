# microDELTA
Human gut microbiome is highly dynamic along the life span. Though human gut microbial community patterns could partly represent the stage-specific or status-specific phenotype of the hosts, the underlying association between gut microbial communities and time-related factors remains unclear, making life trajectory of host based on gut microbial communities difficult. 

In this study, we used microDELTA, a deep learning method based on neural network and transfer learning, for tracking the longitudinal microbial community alterations in diverse contexts. We demonstrated the use of microDELTA to accurate modeling for dynamic patterns of human gut microbial communities at several life stages, including infancy, middle age and the elderly. First, we used microDELTA to illustrate the influence of delivery mode on infant gut microbial communities based on an infant cohort. Second, we examined the spatial-temporal dynamic pattern of gut microbial communities for long-term dietary shifts during international travel based on a Chinese traveler cohort. Third, we explored the seasonal dynamic patterns of gut microbial communities for the Hadza hunter-gatherers. Finally, we analyzed the distinctive gut microbial pattern for elderly people. The analyses of these contexts elucidate how well the transfer learning model-based approach can utilize human gut microbial communities for human life trajectory analysis, which is critical for microbial community- based context-aware health monitoring and clinical practice.

## Pipeline
![](microDELTA.png)

## Example
We take the Chinese traveler cohort as an example to describe the input data of microDELTA.
### Input files
* A `txt` file contains the overall status of the hosts named `microbiomes.txt`. The data in this file is shown below, `root:host_status`
```
root:BJN
root:TT
```
* A `csv` file contains the metadata of the hosts named `SourceMapper.csv`. The first column named `SampleID` contains the index of each host. The second column named `Env` contains the status of each host.
```
SampleID,Env
host1,status1
host2, status2
...,...
```
* Two `tsv` files contain the abundance of gut microbial communities of each host named `Source.tsv` and `Query.tsv`. The columns represent hosts and the rows represents features. We consider `Source.tsv` for training and `Query.tsv` for validating. 
```
#OTU ID host1, host2    ...
microbe1    0   0   ...
microbe2    0   0   ...
... ... ...
```
### running microDELTA
* To performance microDELTA analysis, running the bash script `transfer.sh` . The base model has been put into `aging/mst/model/base_model`
```
sh transfer.sh
```
* To performace Neural Network analysis, Running the bash script `NN.sh`.
```
sh NN.sh
```
* To performance Random Forest analysis, running the python script `RF_traveler.py` in `traveler/RF`.
```
python RF_traveler.py
```
import pandas as pd

if __name__ == '__main__':
    original_data = pd.read_csv('file_report.txt', sep='\t')
    sample_id = []
    absolute_filepath = []
    direction = []
    for i in original_data['run_accession']:
        sample_id.append(i)
        sample_id.append(i)
        absolute_filepath.append(f'/home/zhanghaohong/qiime2_OTU/PRJEB38986/{i}_1.fastq.gz')
        absolute_filepath.append(f'/home/zhanghaohong/qiime2_OTU/PRJEB38986/{i}_2.fastq.gz')
        direction.append('forward')
        direction.append('reverse')
    pd.DataFrame(list(zip(sample_id, absolute_filepath, direction)), 
                 columns=['sample-id', 'absolute-filepath', 'direction']).to_csv('manifest.txt',
                                                                                 sep=',',
                                                                                 index=0)
    
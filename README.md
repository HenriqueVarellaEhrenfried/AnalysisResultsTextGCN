# Description of the repository

Basic_Statistics:
>       Results from MR
>       Results from Ohsumed
>       Results from R52
>       Results from R8

Comparisons
>       all_results[.csv | .xlsx] - Comparisons between the results of Yao and the results achieved in the experiment
>       best_results.csv - Comparisons between the results of Yao and the best results achieved in the experiment
>       statistical_results_between_results.csv - Statistical test between all experiments executed

[MR | Ohsumed | R52 | R8]
>       - RUN [ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ] - The results of the experiment from the model.


Create_Folders.sh - Script to organize original data
CreateCSV.sh - Script to create CSV of Basic_Statistics folder
Data_visualization.ipynb - Script to create other metrics and charts
Parameters_used.csv - File with each parameter used
requirements.txt - All libraries used.


>**Important:** Experiments Ohsumed (exp 17 and 18) and R52 (exp 18) were executed in a CPU instead of a GPU. The GPU available to experiment did not have enough VRAM to run them.


Example to run

```bash
python CreateCSV.py "/mnt/b/Documentos/Doutorado/Resultados_TextGCN/"
```

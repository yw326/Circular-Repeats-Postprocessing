# Cicular Repeats Postprocessing

## Purpose
This program processes the output from [Circular Repeats Finder](https://github.com/yw326/Circular-Repeat-Finder). It removes the overlapping and duplicated data, and provide summary information such as microhomology, GC content and length distribution. 

## Prerequisites

You need to have the output from running the [Circular Repeats Finder](https://github.com/yw326/Circular-Repeat-Finder) (CRF), as well as the DNA sequence file used in CRF.


## Usage

The program takes the following argument
* `--seq_path`: the path to the DNA sequence file
* `--data_path`: the path to the circular repeated pairs data. This could be either a file, or a folder containing all the data files.
* `--output_path`: the output folder that will be created to store the summary data and processed circular repeats data.
* `--is_inverted`: use this flag if inverted circular repeats are processed; default is false (i.e. default is direct circular repeats)
* `--is_data_file`: use this flag if you only want to process a single file. Without this flag, we assume `data_path` is a folder containing all the circular repeat files.

You can also overwrite some default processing parameters. 
* `--no_remove_pair_dup`: use this flag if you don't want to remove duplicated pairs
* `--no_remove_pair_overlap`: use this flag if you don't want to remove overlapped pairs
* `--no_faver_microhomology`: use this flag if you don't want to give priorities for circular repeated pairs that satisfies microhomology
* `--no_remove_segments_overlap`: use this flag if you don't want to remove overlapped segments



## Example

```
python main.py --seq_path sequence.txt --data_path direct_index.txt --output_path output --is_data_file --is_inverted
```

The above command will process all the data in file `direct_index.txt` and creates a folder named `output` in which processed data are stored. Note that (1) file `sequence.txt` holds the DNA sequence data corresponding to the `direct_index.txt` (i.e. `direct_index.txt` is obtained by running `sequence.txt` on CRF), and (2) the type of circular repeats is specified as inverted.

```
python main.py --seq_path sequence.txt --data_path index_data_dir --output_path output 
```

The above is very similar to the previous command. The difference is that this command aggregates the data from all the data files in the directory, and then performs processing. Also, the type of circular repeats is assumed to be direct since `is_inverted` is not set.

## Output Files

Two folders are created by the program: `pairs` and `segments`. Both folders have a pickle file (`summary.pickle`), which stores summary info as a dictionary.

The `pairs` folder stores processed circular repeated pairs data (which removes duplicates and overlap if specified) in a `.csv` file, and saves an image of microhomology length distribution plot. 

The `segments` folder stores processed circular repeated segments data, which are obtained by breaking all the circular repeated pairs (i.e. each pair yields two segments). The program removes overlap if specified. The data is stored in a `.csv` file. A plot of GC content distribtion and a plot of length distribution are also saved in this folder. 






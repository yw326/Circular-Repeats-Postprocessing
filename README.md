# MicroDNA_Detection_Post_Process

The goal of this small python program is to process the result from https://github.com/yw326/MicroDNA_Detection. More specifically it
* filters out the microDNA pairs that has a tandem repeat percentage above a certain predefined threshold.
* write the results in specified output files.
* collect general information on the microDNA pairs found: average GC content, length distribution, and percentage of microDNA with microhomology (2 length).

## Prerequisites

First, you need to have the output sequence and index files obtained from the MicroDNA_Detection https://github.com/yw326/MicroDNA_Detection, as they are required inputs for this program.

Second, use tandem repeat finder (TRF) (https://tandem.bu.edu/trf/trf.html) to obtain a masked version of the original sequence used in MicroDNA_Detection (i.e. tandem repeats in the sequence are replaced with letter "N"). If the original sequence contains letters other than "A", "T", "C", "G", we recommend remove these letters before running TRF.

## Command Line Options

The program has 7 arguments, all required:
* First argument:  sequence file name. It should be the same file used in MicroDNA_Detection.
* Second argument: masked sequence file name. The masked version of the orginal sequence by TRF.
* Third argument: threshold for tandem repeats percentage. Any circle repeats found that has tandem repeats more than this threshold are filtered out. The value should be between 0 and 1.
* Fourth argument: circle repeat sequence file name. The result circle repeat sequence file (from MicroDNA_Detection).
* Fifth argument: circle repeat index file name. The result circle repeat index file (also from MicroDNA_Detection) corresponding to the above result sequence file.
* Sixth argument: output sequence file name.
* Seventh argument: output index file name.


## Example

```
python main.py data/chrY/chrY_prefiltered.txt data/chrY/chrY_prefiltered.mask 0.3 data/chrY/"1st-type cr seq" data/chrY/1st-type_circle_repeat data/chrY/output_seq_file.txt data/chrY/output_idx_file.txt 
```

## Output Files
The output sequence file contains the string of the first section of circle repeats (i.e. s1s2) after tandem repeats filtering.

The output index file contains index info of the circle repeats after tandem repeats filtering. Please check https://github.com/yw326/MicroDNA_Detection/blob/master/README.md for explanation of the index file notation.






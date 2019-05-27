## Prerequisites

You need to have the output index file obtained from https://github.com/yw326/MicroDNA_Detection, as they are required inputs for this program.

# MicroDNA Detection Result Processing

The goal of this small python program is to process the result from https://github.com/yw326/MicroDNA_Detection. More specifically it:
* convert the index file into an array of CircleRepeatPair objects that are easier to process, each of which represents a microDNA reintegration
* filters out duplicated microDNA pairs
* collect general information on the microDNA pairs found: average GC content, length distribution, and information about microDNA with microhomology (2 length).


<!---
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
-->





# Cicular Repeats Postprocessing

## Purpose
This program processes the output from [Circular Repeats Finder](https://github.com/yw326/Circular-Repeat-Finder). More specifically, it removes the overlapping and duplicated data, and provide summary information such as microhomology, GC content and length distribution. 

## Prerequisites

You need to have the output from running the [Circular Repeats Finder](https://github.com/yw326/Circular-Repeat-Finder) (CRF), as well as the DNA sequence file used in circular repeats finder.


# Usage

The program has 7 arguments, all required:
* First argument:  sequence file name. It should be the same file used in MicroDNA_Detection.
* Second argument: masked sequence file name. The masked version of the orginal sequence by TRF.
* Third argument: threshold for tandem repeats percentage. Any circle repeats found that has tandem repeats more than this threshold are filtered out. The value should be between 0 and 1.
* Fourth argument: circle repeat sequence file name. The result circle repeat sequence file (from MicroDNA_Detection).
* Fifth argument: circle repeat index file name. The result circle repeat index file (also from MicroDNA_Detection) corresponding to the above result sequence file.
* Sixth argument: output sequence file name.
* Seventh argument: output index file name.


## Example


## Output Files





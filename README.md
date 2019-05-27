## Prerequisites

You need to have the output index file obtained from https://github.com/yw326/MicroDNA_Detection, as they are required inputs for this program.

# MicroDNA Reintegration Simulation

We simulate microDNA reintegration by iteratively inserting pairs of (s1s2,s2s1) (and (s1s2, s1's2') for reversed complement) into a random string of A, T, C, and G. We also iteratively add mutations (insertion, deletion, replacement) into the sequence. We keep track and update the positions of microDNA repeated pairs after each mutation and microDNA insertion. The output of the simulation are:
(1) a sequence file, which contains the inserted microDNA pairs and mutations
(2) a pickle file contains the information of the positions of the inserted microDNA pairs

In addition, we also provide a testing program that compares the output index file (from using https://github.com/yw326/MicroDNA_Detection) on the simulated sequence to the ground truth (the pickle file containing positions of miroDNA pairs). The program outputs what percentage microDNAs are actually found.


## Command Line Options for Simulation
The program generate_simulation.py has 7 required arguments and 2 optional argument:
* seqlen: length of the simulated sequence before
* num_crepeats: number of microDNA reintegrations to be simulated
* min: minimum of s1 and s2
* max: maximum of s1 and s2
* num_mutations: number of mutations to be added to the sequence
* output_seq_file: the path of output sequence file
* output_crepeats_file: the path of output pickle file that contains locations of microDNA pairs 
* reversed_compl (optional): indicating inserting pairs of (s1s2, s1's2') rather than (s1s2, s2s1); no argument needed
* maxitr (optional): maximum amount of attempts to insert a microDNA pair (default 1000)

## Example for Simulation

```
python generate_simulation.py --seqlen 10000000 --num_crepeats 300 --min 200 --max 500 --maxitr 1000 --num_mutations 200000 --output_seq_file my_output_seq.txt --output_crepeats_file my_repeats_info.pickle —reversed_compl
```

## Command Line Options for Simulation Results Checking
The program check_simulation_result.py has 4 required arguments:
* seq_file: the path of the sequence file
* ground_truth_file: the path of the pickle file that contains locations of microDNA pairs 
* found_file_name: the path of the index file from program https://github.com/yw326/MicroDNA_Detection
* off_allowed: the allowed error rate for the microDNA found compared to the ground truth; for example, if it's set to 0.05, the allowed error is 0.05(length of microDNA), meaning the a detected microDNA pair is counted as a match if its length and positions are within the 0.05(length of microDNA) neighborhood of the ground truth.

## Example for Simulation Results Checking

```
python check_simulation_result.py --seq_file my_seq.txt --ground_truth_file my_repeats_info.pickle --found_file_name my_index.txt --off_allowed 0.05
```


# MicroDNA Detection Result Processing

This project also provides a program to process the result from https://github.com/yw326/MicroDNA_Detection. More specifically it:
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





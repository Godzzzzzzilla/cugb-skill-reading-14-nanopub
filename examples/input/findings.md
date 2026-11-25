# Findings

Sparse routing reduces inference cost by 0.7x on 32k-token contexts.
The router does not increase perplexity on the validation split.
Block-sparse attention improves recall by 3.2 points over dense attention in our reproduction.
Dropout of 0.1 stabilises training but slows convergence by 12%.
The reported ceiling of 92.4% was not reproduced under the original schedule.
Table 2 shows a 23.4% yield increase for the treatment group relative to the control.

# GermEval 2017 modification

This repo modifies the errors of original GermEval 2017 XML file. With publication of it, we encourage researchers experimenting on GermEval 2017 dataset to use this modified version.

A fixed version is already included under the data directory. But you can always use modifyGermEval17.py to go through the errors again. To execute, run the following command:


python modifyGermEval17.py


The code will read in 4 XML file in data directory and fix the following questions:

    1.There are some incomplete tags. Remove them completely and fill with null tag if needed.
    2.Change mispelled polarity to correct spelling
    3.Some target terms are inconsistent with their offset, correct and find the first match. Repetition of the same word is recorded in lef-to-right order. Diachronic testset has 'to2' attribute which will be handled differently.

A modified version will be saved with prefix 'fixed_' + original filename

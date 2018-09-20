import argparse, os
import numpy as np
import pandas as pd

## we want a script that assigns Josh's sample numbers to our plant 
## IDs, and duplicates where necessary (some plants will end up 
## with >1 row because they had multiple samples)

## accepts two imputs: 

## 1) a CSV with two columns: 1 - Josh's samples, 2 - name of Plant to which that sample belongs

## 2) Our phenotype data, by plant.

## This will output a phenotype spreadsheet with josh's sample names correctly
## mapped to 

## additionally, if more than one sample exists, a new row will be created for that plant

## so the sample unit here is one of Josh's samples

## we'll put a default dictionary here in the script but allow the user to input a
## new one as a csv in case this becomes outdated:

parser = argparse.ArgumentParser()
parser.add_argument("Phenotype data",
                type=str,
                help=('CSV, of our phenotype data.'
                        ' Rows are plants.')
                )
parser.add_argument("--map", 
            type=str,
            help= ('CSV, with the first'
            ' column are Josh\'s sample names'
            ' and the second columns are plant'
            ' names. Rows are Josh\'s samples') 
                )


args = parser.parse.args()

#!/usr/bin/env python3 

import os, pickle, argparse, pathlib
import numpy as np
import pandas as pd

## deal with args:
parser = argparse.ArgumentParser()
parser.add_argument('picklefile',
            help=("""The pickled pandas dataframe of our raw 
                    phenotype. Use full path if this script is 
                    not located in the current folder.
                   """))
parser.add_argument('outCSV',
            help=("""The name of the outputted CSV for use with
                    Tassle.
                    """))

args = parser.parse_args()

pickleFile=pathlib.Path(args.picklefile)
#pickleFile=args.picklefile
outCSV=pathlib.Path(args.outCSV)

##get our python file for this data (could use the CSV instead)
rawDataDF = pickle.load(open(pickleFile, "rb"))
## clean up 
del rawDataDF['geojson']
## split out the petal types
uppersRaw = rawDataDF[rawDataDF.petalName != 'right'].copy()
lowerRaw = rawDataDF[rawDataDF.petalName == 'right'].copy()
## group by flowers for upper petal, average the upper petals
uppersMean = uppersRaw.groupby(['plantName','flowerName']).mean()
## clean up new columns 
uppersMean.reset_index(inplace = True)
## add petalName back in (dropped above)
uppersMean['petalName'] = 'upper'
lowerRaw['petalName'] = 'lower'
## concatenate by row
combRaw = pd.concat([ uppersMean, lowerRaw ], sort=True)
## take the average of each petal type nested within each plant
plantDf = combRaw.groupby(['plantName','petalName']).mean()
## localized transpose
meliaData = plantDf.unstack(level=1)
## collapse the hierarchical labels
newName = ['_'.join(col).strip() for col in meliaData.columns.values] 
meliaData.columns = newName
meliaData.to_csv(outCSV, na_rep='NaN')


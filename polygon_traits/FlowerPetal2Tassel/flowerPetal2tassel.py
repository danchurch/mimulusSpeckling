#!/usr/bin/env python3 

import os, pickle
import numpy as np
import pandas as pd

##get our python file for this data (could use the CSV instead)
pickleFile="flowerPetalDF_27.11.2018.p"
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
meliaData.to_csv('automatedResuls_forTassle_27.11.2018.csv', na_rep='NaN')

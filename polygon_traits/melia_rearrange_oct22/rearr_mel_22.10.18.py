import os, pickle
import pandas as pd
import numpy as np 

rawDataDF = pd.read_csv('Oct20_RedData.csv')

## fix names:

aa = rawDataDF.rename(columns = {'Upper Left' : 'Upper_Left', 
                           'Upper Right': 'Upper_Right'})

## are all names unique?

len(aa.Name.unique()) ## hmm. There's a repeat somewhere...
aa.Name.duplicated() ## looks like the last one. 
aa.tail() ## does look like duplicated data. Remove
aa = aa[:-1]
                
## we want to average the upper petals:
aa['upper_mean'] = aa[['Upper_Left', 'Upper_Right']].mean(axis=1)

aa.drop(['Upper_Left','Upper_Right'], 1, inplace = True)

## now, we need to average the plants... this is tricker, we gotta
## parse the names a little...

## all names start with a P, then 3 digits, then F + number.
## We want to lump by the three digits:

aa['plant_name'] = aa.Name.str.extract('(P[0-9]{3})', expand=False)

## seems to work. Can we group by this?
bb = aa.groupby(['plant_name']).mean()

## I think this is what we want? rename columns:

bb.rename(columns = { 'Lower' : 'propRed_lower',
                    'upper_mean' : 'propRed_upper'},
                    inplace = True )

## write to csv 

bb.to_csv("Melia_propRed.22.10.2018.csv")

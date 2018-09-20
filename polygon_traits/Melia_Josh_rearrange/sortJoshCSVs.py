#!/usr/bin/env python3

import argparse, os, csv, pickle
import numpy as np
import pandas as pd


def makeMDict(mappFile):
    ''' make a dictionary from our map of Josh's samples'''
    mapp =  pd.read_csv(mappFile, header=None, dtype=str)
    mapp.columns = 'Sample', 'Plant'
    mapp.set_index('Sample', inplace = True)
    mappDic = mapp.T.to_dict('list')
    return(mappDic)

def makePDict(phenoFile):
    ''' make a dictionary from our phenotype CSV'''
    pheno =  pd.read_csv(phenoFile)
    ## change plant names to match index, get rid of "P":
    pheno.plantName = pheno.plantName.str.replace('P','')
    pheno.set_index('plantName', inplace=True)
    phenDic = pheno.to_dict('index')
    return(phenDic)

def makeNewDf(PDict, MDict):
    ''' make a dataframe from the mapping and phenotype dictionaries'''
    bagOfDicts = []
    for i in MDict:
        newRow = {'sample':i,'plantName':MDict[i][0]}
        oldRow = PDict[MDict[i][0]]
        mergedD = {**newRow , **oldRow}
        bagOfDicts.append(mergedD)
    pandaDict = pd.DataFrame(bagOfDicts)
    pandaDict = pandaDict.set_index('plantName').reset_index()
    pandaDict = pandaDict.set_index('sample')
    return(pandaDict)


## deal with command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("phenoData",
                type=str,
                help=('CSV, of our phenotype data.'
                        ' Rows are plants.')
                )

parser.add_argument("--map", 
            type=str,
            help= ('CSV, with the first'
            ' column are Josh\'s sample names'
            ' and the second columns are plant'
            ' names. Don\t use column names.'
            ' Rows are Josh\'s samples.'),
            default=(
                    os.getcwd() + 
                    "/" + "mapSample2plant.csv"
                            )
            )

parser.add_argument("--outputName",
            type=str,
            help=('Name of the reformatted CSV file.'
            ' Goes to stdout if no name given.'),
                )
args = parser.parse_args()

## organize names a litte:
phenoFile = args.phenoData
mappFile = args.map
if args.outputName is None:
    OutCSV=('modified_' + args.phenoData)
    OutPickle = OutCSV.replace("csv","p")
else:
    OutCSV = args.outputName
    OutPickle = OutCSV.replace("csv","p")

## run our functions
ph = makePDict(phenoFile)
ma = makeMDict(mappFile)
df = makeNewDf(ph,ma)

## create csv and pickled dataframe:
df.to_csv(OutCSV, na_rep='NaN')

pickle.dump(df, open(OutPickle, "wb"))

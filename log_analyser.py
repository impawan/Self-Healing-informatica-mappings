# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:35:07 2019

@author: paprasad
"""



import numpy as np
import pandas as pd


error_matrix = list()

log = open('logs.txt', 'r')

log = log.read()
log = log.split('\n')
for row in log:
    if ': ERROR :' in row:
        print(row) 
        error_matrix.append(row.split(':'))



df = pd.DataFrame(error_matrix)
print(df)
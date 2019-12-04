# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:17:24 2019

@author: paprasad
"""
n= 15000
cnt = 0
for i in range(1,n):
    for j in range(1,n):
        if i*i*i == j*j:
            cnt = cnt+1
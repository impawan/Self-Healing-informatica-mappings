# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:35:07 2019

@author: paprasad
"""



import numpy as np
import pandas as pd
from xml.dom import minidom
from lxml import etree

error_matrix = list()

log = open('logs.txt', 'r')

log = log.read()
log = log.split('\n')
for row in log:
    if ': ERROR :' in row:
        error_matrix.append(row.split(':'))



df = pd.DataFrame(error_matrix)

mapping_xml  = open('m_CrDbStatsment.xml','r')

mapping_xml = mapping_xml.read()


def modify_xml(mapping_xml):
#    doc = minidom.parse("m_CrDbStatsment.xml")
#    name = doc.getElementsByTagName("CONNECTOR")[0]
#    print(name.nodeName)
    root = etree.fromstring(mapping_xml)
    etree.tostring(root)
    
    
    
    
modify_xml(mapping_xml)
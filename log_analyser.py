# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:35:07 2019

@author: paprasad
"""



import numpy as np
import pandas as pd
from lxml import etree
from io import StringIO, BytesIO
import re





error_matrix = list()

log = open('logs.txt', 'r')

log = log.read()
log = log.split('\n')
for row in log:
    if ': ERROR :' in row:
        #print(row) 
        error_matrix.append(row.split(':'))



df = pd.DataFrame(error_matrix)

file = 'm_CrDbStatsment.xml'

           
                            
               
##
def xml_formation(file):
    mapping_xml = open(file,'r')
    mapping_xml = mapping_xml.read()
    mapping_xml = mapping_xml.replace('\n', ' ').replace('\r', '')
    m = re.search('(<REPOSITORY.*DATABASETYPE="Oracle">)(.*)(<\/REPOSITORY>)', mapping_xml)
    mapping_xml = m.group(2)
    return mapping_xml

mapping_xml = xml_formation(file)

 
def fix_data_type(mapping_xml,port_name, data_type):
    XMLtree = etree.parse(StringIO(mapping_xml))
    node_list = list()
    for node in XMLtree.xpath('//CONNECTOR[@FROMFIELD=\'Branch_code\']'):
        instance_name = node.xpath('./@FROMINSTANCE')[0]
        instance_type = node.xpath('./@FROMINSTANCETYPE')[0]
        node = [instance_name,instance_type]
        node_list.append(node)
    print(node_list)
        
        
        
fix_data_type(mapping_xml,'ffs','ff')    
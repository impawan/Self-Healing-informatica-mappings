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

file = 'm_CrDbStatsment_orginal.xml'

           
                            
               
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
    #LList = LinkedList()
    
    #aandeel = tree.xpath('//a[@title="%s"]/text()' % var)
    node = XMLtree.xpath('//CONNECTOR[@FROMFIELD="%s"]'% port_name)[0]
    while(node is not None):
        FROMINSTANCE = node.xpath('./@FROMINSTANCE')[0]
        FROMINSTANCETYPE = node.xpath('./@FROMINSTANCETYPE')[0]
        TOFIELD = node.xpath('./@TOFIELD')[0]
        TOINSTANCE = node.xpath('./@TOINSTANCE')[0]
        lnode = [FROMINSTANCE,FROMINSTANCETYPE,TOFIELD,TOINSTANCE]
        node_list.append(lnode)
        new_xpath = '//CONNECTOR[@FROMFIELD=\''+TOFIELD+'\'][@FROMINSTANCE=\''+TOINSTANCE+'\']'
        node = XMLtree.xpath(new_xpath)
        
        if len(node) == 0 :
            break
        else:
            node = node[0]
        
       
    #print(node_list)         
    print(node_list)    
    for i in node_list:
        if i[1]=='Source Definition':
            node = XMLtree.xpath('//SOURCE[@NAME="%s"]' % i[0])[0]
            node = node.xpath('./SOURCEFIELD[@NAME="%s"]' % i[2])[0]
            node.set('DATATYPE' ,'number')
            print(etree.tostring(XMLtree,pretty_print=True))
#    for node in XMLtree.xpath('//CONNECTOR[@FROMFIELD=\'Branch_code\']'):
#        instance_name = node.xpath('./@FROMINSTANCE')[0]
#        instance_type = node.xpath('./@FROMINSTANCETYPE')[0]
#        node = [instance_name,instance_type]
#        node_list.append(node)
#        LList.insertEnd(node)
    #print(node_list)
    #LList.printList()
     
        
        
        
fix_data_type(mapping_xml,'Branch_code','ff')    
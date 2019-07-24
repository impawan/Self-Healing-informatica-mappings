# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:35:07 2019

@author: paprasad
"""



import numpy as np
import pandas as pd
from lxml import etree,objectify
from io import StringIO, BytesIO
import re



XML_metaData = '''<?xml version="1.0" encoding="Windows-1252"?>
<!DOCTYPE POWERMART SYSTEM "powrmart.dtd">
<POWERMART CREATION_DATE="07/23/2019 12:36:42" REPOSITORY_VERSION="184.93">
<REPOSITORY NAME="INFA_REP" VERSION="184" CODEPAGE="MS1252" DATABASETYPE="Oracle">'''

XML_end = '''</REPOSITORY>
</POWERMART>'''
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

           
def validate(xmlschema_doc) -> bool:
    dtd_file = open("C:/Informatica/9.6.1/server/bin/powrmart.dtd",'rb')
    dtd_file = dtd_file.read()
    
    dtd = etree.DTD(dtd_file)
    tree = objectify.parse(xmlschema_doc)
    print (dtd.validate(tree))
    xmlschema = etree.XMLSchema(StringIO(xmlschema_doc))

  
    result = xmlschema.validate(xmlschema)

    return result
             
               
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
    
    node = XMLtree.xpath('//CONNECTOR[@FROMFIELD="%s"]'% port_name)[0]
    while(node is not None):
        FROMINSTANCE = node.xpath('./@FROMINSTANCE')[0]
        FROMINSTANCETYPE = node.xpath('./@FROMINSTANCETYPE')[0]
        FROMFIELD = node.xpath('./@FROMFIELD')[0]
        TOFIELD = node.xpath('./@TOFIELD')[0]
        TOINSTANCE = node.xpath('./@TOINSTANCE')[0]
        lnode = [FROMINSTANCE,FROMINSTANCETYPE,FROMFIELD,TOFIELD,TOINSTANCE]
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
            
            
        else:
            
            node = XMLtree.xpath('//TRANSFORMATION[@NAME="%s"]' % i[0])[0]
            node = node.xpath('./TRANSFORMFIELD[@NAME="%s"]' % i[2])[0]
            node.set('DATATYPE' ,'decimal')
        
    fixed_XML =  etree.tostring(XMLtree,pretty_print=True).decode("utf-8") 
    fixed_XML = XML_metaData+fixed_XML+XML_end
    writeXML = open("fixed.xml","w")
    writeXML.write(fixed_XML)
    writeXML.close()

        
        
fix_data_type(mapping_xml,'Branch_code','ff')    
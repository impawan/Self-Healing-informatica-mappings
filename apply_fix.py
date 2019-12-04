# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:43:09 2019

@author: paprasad
"""



import time
from lxml import etree,objectify
from io import StringIO, BytesIO
import re

def find_port(error_msg):
    port = re.findall(r'\[(.*?)\]*?(\[(.*?)\])',error_msg,re.M|re.I)
    port = port[0]
    return port[2]
    
    
    
    
def fix_data_type(arg):
    
    XML_end = '''</REPOSITORY>
    </POWERMART>'''
    XML_metaData = '''<?xml version="1.0" encoding="Windows-1252"?>
<!DOCTYPE POWERMART SYSTEM "powrmart.dtd">
<POWERMART CREATION_DATE="07/23/2019 12:36:42" REPOSITORY_VERSION="184.93">
<REPOSITORY NAME="INFA_REP" VERSION="184" CODEPAGE="MS1252" DATABASETYPE="Oracle">'''

    mapping_xml = arg[0]
    error_msg = arg[1]
    XMLtree = etree.parse(StringIO(mapping_xml))
    node_list = list()
    
    port_name = find_port(error_msg)
   
    #node = XMLtree.xpath('//CONNECTOR[@FROMFIELD="%s"]'% port_name)[0] #Find all the ports which are connected to 
    ##//CONNECTOR[@FROMFIELD='Branch_code'][@FROMINSTANCE ='src_ff_mon_statement']
    ##//CONNECTOR[@FROMFIELD="%s"][@FROMINSTANCE ="%s"]
    #source_definitions = //SOURCE[./SOURCEFIELD/@NAME = 'Branch_code']/@NAME
    source_definitions =  XMLtree.xpath('//SOURCE[./SOURCEFIELD/@NAME = "%s"]/@NAME'% port_name)[0]
    print(source_definitions)
    #node = XMLtree.xpath('//CONNECTOR[@FROMFIELD="%s"]'% port_name)[0] #FROMINSTANCETYPE ="Source Definition" 
    print('\n\n\n**fetching all the transformation which are connected to port ',port_name)
    node = XMLtree.xpath('//CONNECTOR[@FROMFIELD="%s"][@FROMINSTANCE ="%s"]'% (port_name,source_definitions))[0]
    while(node is not None):
        time.sleep(0.5)
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
        
    ## Handle the last node
    last_Transformation = node_list[-1][-1]
    last_Field = node_list[-1][-2]
    
    last_node = [last_Transformation,'Dummy',last_Field,'Dummy']
    node_list.append(last_node)
    
    print('\n\n\n***Aplying fix on transformation :-') 
    for i in node_list:
        time.sleep(0.5)
        print('\n\n Adjusting transformation ',i[0], ' for port ',i[2])
        if i[1]=='Source Definition':
            node = XMLtree.xpath('//SOURCE[@NAME="%s"]' % i[0])[0]
            node = node.xpath('./SOURCEFIELD[@NAME="%s"]' % i[2])[0]
            node.set('DATATYPE' ,'string')
            
            node = 'null'
            
            
        else:
            
            node = XMLtree.xpath('//TRANSFORMATION[@NAME="%s"]' % i[0])[0]
            node = node.xpath('./TRANSFORMFIELD[@NAME="%s"]' % i[2])[0]
           
            node.set('DATATYPE' ,'string')
            node = 'null'
    mapping_name =  XMLtree.xpath('//MAPPING/@NAME')[0]
    fixed_XML =  etree.tostring(XMLtree,pretty_print=True).decode("utf-8") 
    fixed_XML = XML_metaData+fixed_XML+XML_end
    fixed_xml_file = './corr_mapping//'+mapping_name+'.xml'
    writeXML = open(fixed_xml_file,"w")
    writeXML.write(fixed_XML)
    writeXML.close()
    print('\n\n\n***Mapping is fixed, XMl file is ',fixed_xml_file)
    
    
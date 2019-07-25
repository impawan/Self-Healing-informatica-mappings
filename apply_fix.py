# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:43:09 2019

@author: paprasad
"""

from lxml import etree,objectify
from io import StringIO, BytesIO


def find_port(error_msg):
    
    
    
    
def fix_data_type(mapping_xml,erro_msg):
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
            node.set('DATATYPE' ,'string')
            
            
        else:
            
            node = XMLtree.xpath('//TRANSFORMATION[@NAME="%s"]' % i[0])[0]
            node = node.xpath('./TRANSFORMFIELD[@NAME="%s"]' % i[2])[0]
            node.set('DATATYPE' ,'string')
        
    fixed_XML =  etree.tostring(XMLtree,pretty_print=True).decode("utf-8") 
    fixed_XML = XML_metaData+fixed_XML+XML_end
    fixe_xml_file = mapping_xml+'.xml'
    writeXML = open(fixe_xml_file,"w")
    writeXML.write(fixed_XML)
    writeXML.close()
    print('Mapping is fixed, XMl file is ',fixe_xml_file)
    
    
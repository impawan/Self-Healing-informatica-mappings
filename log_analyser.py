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

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self,head):
        self.head = head
    
    
    def getN(self,position):
        temp = self.head
        counter = 0 
        while(temp):
            if counter == position:
                return temp
            temp = temp.next
            counter = counter + 1
 
    #This method finds the last node of the Linked List 
    def findLastNode(self):
        temp = self.head
        while(temp):
            if(temp.next is None):
                return temp
            else:
                temp = temp.next 
        
    #Insert at the beginnning of Linked List 
    def push(self,data):
        node_head = Node(data)
        node_head.next = self.head
        self.head = node_head
        print('\nNode ',data,' added!\n')
    
    #Insert in the end of the Linked List 
    def insertEnd(self,data):
        #find the last node
        lastNode = self.findLastNode()
        newLastNode = Node(data)
        lastNode.next = newLastNode
        
     #Insert after a given Node   
    def InsertAfter(self,posNode,data):
        if posNode is None:
            print('Invalid Node - Node not in Linked In')
            return
        else:
            new_node = Node(data)
            new_node.next = posNode.next
            posNode.next = new_node  
    
    def deleteNode(self,data):
        temp  = self.head
        found_flag = False 
        if temp.data == data:
            self.head = temp.next
            temp = None
            return
        prev = Node(None)
        while(temp is not None):
            if temp.data == data:
                prev.next = temp.next
                temp = prev
                found_flag = True
            prev = temp
            temp = temp.next
        
        if found_flag is False:
            print('No Node ',data,' found in the Linked List\n')
    
    def positionalDelete(self, position):
        temp = self.head
        if position == 0:
            self.head = temp.next
            temp = None
            print('Deleted the Node at head position')
            return 
        else:
            for i in range(position-1):
                temp = temp.next
                if temp is None:
                    break
                
                
            if temp is None or temp.next is None:
                print('Given position is greater than Linked List length')
                return
            else:
                delNode = temp.next
                temp.next = delNode.next
                del delNode.data
               
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
   # root = etree.XML(XMLtree)
    head_node = XMLtree.xpath('//CONNECTOR[@FROMFIELD=\'Branch_code\']/@FROMFIELD')[0]
    
    print(head_node)
    
    
fix_data_type(mapping_xml,'ffs','ff')    
import numpy as np
import scipy.stats as ss
import csv
from nodes import *

MARKETVALUE = 10000000
PRIORS = np.array([0.2,0.2,0.2,0.2,0.2])
MARKETSHARES = np.array([0.3,0.4,0.5,0.6,0.7])
SURVEYCOST = 10250
LIKELIHOODS = np.array([[0.1176,0.0466,0.01563,0.0041,0.00073],[0.3,0.18,0.093,0.036,0.01],[0.32,0.311,0.234,0.14,0.059],[0.185,0.276,0.312,0.276,0.18],[0.059,0.138,0.234,0.311,0.324],[0.01,0.0368,0.093,0.186,0.3]])

class Tree(list):
    def __init__ (self):

        super().__init__()

        self.append(RootNode())#node 0
        self.add_node(parent = self[0],node_class= DecisionNode, value= 'market')#node 1
        self.add_node(parent = self[0], node_class = DecisionNode, value = 'survey')#node 2
        for i in range(6): #nodes 3 to 7
        	self.add_node(parent = self[2], node_class = OutcomeNode, value = i) 

    def add_layer(self):
        for node in self:
            if (not node.children and node.value in range(6)):
                self.add_node(parent = node,node_class =DecisionNode,value ='market')
                self.add_node(parent = node,node_class =DecisionNode,value ='survey')

        for node in self:
            if(not node.children and node.value == 'survey'):
                for k in range(6):
                    self.add_node(parent = node, node_class = OutcomeNode, value =k)

    def end_layer(self):
        for node in self:
            if(not node.children and type(node).__name__!='EndNode'):
                self.add_node(parent = node,node_class = EndNode)

    def add_node(self,parent,node_class,value=None):
        new_node=node_class(parent = parent, value= value)
        self.append(new_node)
        parent.add_child(new_node)

    def posteriors(self):
        for node in self:
            node.posteriors

    def expected_value(self):
        for node in self[::-1]:
            node.expected_value

    def print_tree(self):
        for node in self:
            print(f'node number {node}  node type {node.value}')
            print (f'chidren {node.see_children()}, parent {str(node.parent)}')
            print(f'posteriors {node.posteriors}, ')
            print(f'expected_value {node.expected_value}')






t = Tree()
t.add_layer()
t.end_layer()
t.print_tree()
t.expected_value()
#print(id(t[1].parent), id(t[0]))
#print(t[5])

#print(t[0].children)

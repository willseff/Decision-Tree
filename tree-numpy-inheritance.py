import numpy as np
import scipy.stats as ss
import csv

MARKETVALUE = 10000000
PRIORS = [0.2,0.2,0.2,0.2,0.2]
MARKETSHARES = [0.3,0.4,0.5,0.6,0.7]
SURVEYCOST = 10250
LIKELIHOODS = [[0.1176,0.0466,0.01563,0.0041,0.00073],[0.3,0.18,0.093,0.036,0.01],[0.32,0.311,0.234,0.14,0.059],[0.185,0.276,0.312,0.276,0.18],[0.059,0.138,0.234,0.311,0.324],[0.01,0.0368,0.093,0.186,0.3]]

class Node:
    node_number = 1
    def __init__(self,parent=[],child=[]):
        self.parent = parent
        self.children = child
        self.node_number = Node.node_number

    def add_child(self,node):
    	self.children.append(node)

    def __str__ (self):
    	return f'{self.node_number}'

    def __repr__(self):
    	return node_number

    @property
    def posteriors(self):
        return PRIORS

    def __repr__(self):
        return str(type(self))

    @classmethod
    def increment_node(cls):
    	cls.node_number=+1

class DecisionNode(Node):
    def __init__ (self,parent=None,child=[],value =''):

        super().__init__(parent=parent, child = child)

    @property
    def posteriors(self):
        return self.parent.posteriors
    

class OutcomeNode(Node):
    def __init__ (self,value,parent,child=[]):

        super().__init__(parent=parent, child = child)

        @property
        def posteriors(self):
            priors = self.parent.posteriors
            joint_probablity = priors*LIKELIHOODS[survey_results]
            sum_joint = sum(joint_probablity)
            posteriors = joint_probablity/sum_joint
            return posteriors

class EndNode(Node):
    def __init__ (self,parent=[],child=[],prior_surveys=0):
        child =None
        super().__init__(parent=parent, child = child)

    @property
    def posteriors(self):
    	return self.parent.posteriors
    

class Tree(list):
    def __init__ (self):

        super().__init__()

        self.append(Node(parent=None,child=[]))#node 0
        self.add_node(parent = self[0],child=[],node_class= DecisionNode, value= 'market')#node 1
        self.add_node(parent = self[0],child=[], node_class = DecisionNode, value = 'survey')#node 2
        for i in range(6):
        	self.add_node(parent = self[2],child=[], node_class = OutcomeNode, value = i)

    def add_node(self,parent,child,node_class,value):
    	new_node=node_class(parent = parent, child = child, value= value)
    	self.append(new_node)
    	parent.children.append(new_node)
    	Node.increment_node()





t = Tree()
print(id(t[1].parent), id(t[0]))
print(t[0])

print(t)

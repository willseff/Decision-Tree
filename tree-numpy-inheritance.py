import numpy as np
import scipy.stats as ss
import csv

MARKETVALUE = 10000000
PRIORS = np.array([0.2,0.2,0.2,0.2,0.2])
MARKETSHARES = np.array([0.3,0.4,0.5,0.6,0.7])
SURVEYCOST = 10250
LIKELIHOODS = np.array([[0.1176,0.0466,0.01563,0.0041,0.00073],[0.3,0.18,0.093,0.036,0.01],[0.32,0.311,0.234,0.14,0.059],[0.185,0.276,0.312,0.276,0.18],[0.059,0.138,0.234,0.311,0.324],[0.01,0.0368,0.093,0.186,0.3]])

class Node:
    node_number = 1
    def __init__(self,parent):
        self.parent = parent
        self.node_number = Node.node_number
        self.value = 'root'
        self.children = []

    def add_child(self,node):
    	self.children.append(node)

    @property
    def posteriors(self):
        return PRIORS

    def __repr__(self):
        return str(self.node_number)

    @classmethod
    def increment_node(cls):
    	cls.node_number+=1

    def see_children(self):
        string = ''
        for child in self.children:
            string += str(child) + ' '
        return string



class DecisionNode(Node):
    def __init__ (self,parent,value =''):
        super().__init__(parent=parent)
        self.value = value

    @property
    def posteriors(self):
        return np.copy(self.parent.posteriors)

    @property 
    def expected_value(self):
    	return
    




class OutcomeNode(Node):
    def __init__ (self,parent,value):
        super().__init__(parent=parent)
        self.value=value

    @property
    def posteriors(self):
        priors = self.parent.posteriors
        joint_probablity = priors*LIKELIHOODS[self.value]
        posteriors = joint_probablity/sum(joint_probablity)
        return posteriors

    @property 
    def expected_value(self):
    	pass





class EndNode(Node):
    def __init__ (self,parent,prior_surveys=0):
        child =None
        super().__init__(parent=parent)

    @property
    def posteriors(self):
    	return np.copy(self.parent.posteriors)

    @property
    def expected_value(self):
        expected_value = self.posteriors*MARKETSHARES*MARKETVALUE
        return 
    



    

class Tree(list):
    def __init__ (self):

        super().__init__()

        self.append(Node(parent=None))#node 0
        Node.increment_node()
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

    def add_node(self,parent,node_class,value):
        new_node=node_class(parent = parent, value= value)
        self.append(new_node)
        parent.add_child(new_node)
        Node.increment_node()

    def posteriors(self):
   	    for node in self:
   	        node.posteriors

   	def expected_value(self):
   		for node in self[::-1]
   			node.expected_value

    def print_tree(self):
        for node in self:
            print(f'node number {node}  node type {node.value}')
            print (f'chidren {node.see_children()}, parent {str(node.parent)}')
            print(f'posteriors {node.posteriors}, ')






t = Tree()
t.add_layer()
t.posters()
#print(id(t[1].parent), id(t[0]))
#print(t[5])

#print(t[0].children)

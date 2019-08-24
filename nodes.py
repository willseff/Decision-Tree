import numpy as np
import scipy.stats as ss


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
        self.children = []
        Node.increment_node()

    def add_child(self,node):
    	self.children.append(node)

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

class RootNode(Node):

    def __init__ (self):
        super().__init__(parent = None)
        self.value = 'root'

    @property
    def posteriors(self):
        return PRIORS

    @property
    def expected_value(self):
        return None

class DecisionNode(Node):
    def __init__ (self,parent,value =''):
        super().__init__(parent=parent)
        self.value = value

    @property
    def posteriors(self):
        return np.copy(self.parent.posteriors)

    @property 
    def expected_value(self):
        if self.value == 'market':
            return self.children[0].expected_value
        else:
            children_expected_values=[]
            for child in self.children:
                children_expected_values.append(child.expected_value)
            
            children_expected_values=np.array(children_expected_values)    
            probablities = [0,0,0,0,0,0]
            for j in range(6):
                joint_sum = 0
                for i in range(5):
                    hh = ss.binom(5, MARKETSHARES[i])
                    joint_sum = joint_sum+hh.pmf(j)*self.posteriors[i]
                probablities[j]=joint_sum 

            return probablities*children_expected_values

    




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
    def __init__ (self,parent,prior_surveys=0,**kwargs):
        child =None
        self.value = 'end'
        super().__init__(parent=parent)

    @property
    def posteriors(self):
    	return np.copy(self.parent.posteriors)

    @property
    def expected_value(self):
        expected_value = sum(self.posteriors*MARKETSHARES*MARKETVALUE)
        return expected_value
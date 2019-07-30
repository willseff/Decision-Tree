import numpy as np
import scipy.stats as ss

LIKELIHOODS = [[0,0.4096,0.2592,0.0768,0.0064],[0,0.3,0.423,0.04,0.9],[0,123,0.84,0.41,0.6],[0,0.4096,0.2592,0.7868,0.564],[0,0.396,0.2592,0.568,0.864],[0,0.4696,0.4592,0.665,34]]
MARKETVALUE = 10000000
MARKETSHARES = [0.1,0.2,0.4,0.6,0.8]
def survey_outcome_odds(priors):
	probablities = [0,0,0,0,0,0]
	for j in range(6):
		joint_sum = 0
		for i in range(5):
			hh = ss.binom(5, MARKETSHARES[i])
			joint_sum = joint_sum+hh.pmf(j)*priors[i]
		probablities[j]=joint_sum	
	return probablities

def list_one_multiply(a,b):
	new_list = []
	for i in range(len(a)):
		value = a[i]*b
		new_list.append(value)
	return new_list

def list_multiply(a,b):	
	new_list = []
	for i in range(len(a)):
		value = a[i]*b[i]
		new_list.append(value)
	return new_list

def list_divide(a,d):
	new_list = []
	for i in range(len(a)):
		value = a[i]/d
		new_list.append(value)
	return new_list

class node:
    def __init__(self,p,c,t):

        self.parent = p
        self.children = c
        self.node_type = t
        self.posteriors = []
        self.expected_value = 0
        self.decision=''
        self.history=[]

    def __str__(self):
    	return 'Parent '+str(self.parent)+' Children '+str(self.children) + ' posteriors ' + str(self.posteriors) + 'nodeType ' + str(self.node_type) + ' eValue ' + str(self.expected_value) + ' decision ' + str(self.decision)

    def add_child(self,node):
    	self.children.append(node)

    def add_history(self,event):
    	self.history.append(event)

class tree:
	def __init__(self):
		self.list_of_nodes=[]
		self.list_of_nodes.append(node([],[1,2],'root'))
		self.list_of_nodes.append(node([0],[],'market'))
		self.list_of_nodes.append(node([0],[],'survey'))
		self.list_of_nodes[2].posteriors=[0.2,0.2,0.2,0.2,0.2]
		self.list_of_nodes[1].posteriors=[0.2,0.2,0.2,0.2,0.2]

	def add_node(self,node):
		priors = self.list_of_nodes[node.parent].posteriors
		if (node.node_type in [0,1,2,3,4,5]):
			joint_probablity = list_multiply(priors,LIKELIHOODS[node.node_type])
			sum_joint = sum(joint_probablity)
			node.posteriors = list_divide(joint_probablity,sum_joint)
		else:
			node.posteriors = priors

		if (node.node_type == 'end'):
			values = list_one_multiply(MARKETSHARES,MARKETVALUE)
			node.expected_value = sum(list_multiply(values,node.posteriors))

		self.list_of_nodes.append(node)
		self.list_of_nodes[node.parent].children.append(len(self.list_of_nodes)-1)

	def __str__(self):
		string = ''
		for i in range(len(self.list_of_nodes)):
			string = string + ' node ' +str(i) + ' ' + (str(self.list_of_nodes[i]) + '\n')
		return string

	def node(self,number):
		return self.list_of_nodes[number]

	def len(self):
		return(len(self.list_of_nodes))

	def update_expected_values(self):
		#use after placing end nodes
		#must end with a outcome layer
		for i in reversed(range(len(self.list_of_nodes))):
			print(i)
			if (self.list_of_nodes[i].node_type == 'end'):
				pass
			elif(self.list_of_nodes[i].node_type == 'survey'):
				probablities = survey_outcome_odds(self.list_of_nodes[i].posteriors)
				expected_value=0
				for k in range(6):
					nodek = self.list_of_nodes[self.list_of_nodes[i].children[k]]
					expected_value=expected_value + (probablities[k] * nodek.expected_value)
				self.list_of_nodes[i].expected_value = expected_value

			elif(self.list_of_nodes[i].node_type in range(6)):
				if (self.list_of_nodes[self.list_of_nodes[i].children[0]].node_type=='end'):
					child = self.list_of_nodes[i].children[0]
					self.list_of_nodes[i].expected_value = self.list_of_nodes[child].expected_value
				else:
					child1 = self.list_of_nodes[self.list_of_nodes[i].children[0]]
					child2 = self.list_of_nodes[self.list_of_nodes[i].children[1]]
					if(child1.expected_value>=child2.expected_value):
						self.list_of_nodes[i].decision = 'survey'
						self.list_of_nodes[i].expected_value = child1.expected_value
					else:
						self.list_of_nodes[i].expected_value = child2.expected_value
						self.list_of_nodes[i].decision = 'market'
			elif(self.list_of_nodes[i].node_type == 'market'):
				child = self.list_of_nodes[i].children[0]
				self.list_of_nodes[i].expected_value = self.list_of_nodes[child].expected_value

	def child(self,i,k):
		#returns kth the child node for node i
		return self.list_of_nodes(self.list_of_nodes[i].children[k])

def add_layer(tree,layer_type):
	if (layer_type == 'decision'):
		for i in range(tree.len()):
			if (not tree.node(i).children and tree.node(i).node_type != 'market'):
				tree.add_node(node(i,[],'survey'))
				tree.add_node(node(i,[],'market'))

	if (layer_type == 'outcome'):
		for i in range(tree.len()):
			if (not tree.node(i).children and tree.node(i).node_type == 'survey'):
				for k in range(6):
					tree.add_node(node(i,[],k))

	if(layer_type == 'end'):
		for i in range(tree.len()):
			if (not tree.node(i).children):
				tree.add_node(node(i,[],'end'))

t = tree()
add_layer(t,'outcome')
add_layer(t,'decision')
add_layer(t,'outcome')
add_layer(t,'decision')
add_layer(t,'outcome')
add_layer(t,'end')
t.update_expected_values()
print(t)




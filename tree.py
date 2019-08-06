import numpy as np
import scipy.stats as ss
import csv

#likelyhoods are not correct values right now, Will need to changed based on what the priors are
#LIKELIHOODS = [[0,0.4096,0.2592,0.0768,0.0064],[0,0.3,0.423,0.04,0.9],[0,123,0.84,0.41,0.6],[0,0.4096,0.2592,0.7868,0.564],[0,0.396,0.2592,0.568,0.864],[0,0.4696,0.4592,0.665,34]]
MARKETVALUE = 10000000
PRIORS = [0.2,0.2,0.2,0.2,0.2]
MARKETSHARES = [0.3,0.4,0.5,0.6,0.7]
SURVEYCOST = 10250
LIKELIHOODS = [[0.1176,0.0466,0.01563,0.0041,0.00073],[0.3,0.18,0.093,0.036,0.01],[0.32,0.311,0.234,0.14,0.059],[0.185,0.276,0.312,0.276,0.18],[0.059,0.138,0.234,0.311,0.324],[0.01,0.0368,0.093,0.186,0.3]]
#method to return the odds of each survey result happening based on the probabliities
def survey_outcome_odds(priors):
	probablities = [0,0,0,0,0,0]
	for j in range(6):
		joint_sum = 0
		for i in range(5):
			hh = ss.binom(5, MARKETSHARES[i])
			joint_sum = joint_sum+hh.pmf(j)*priors[i]
		probablities[j]=joint_sum	
	return probablities
#method to multiply a list with one value
def list_one_multiply(a,b):
	new_list = []
	for i in range(len(a)):
		value = a[i]*b
		new_list.append(value)
	return new_list
#method to multupy two lists
def list_multiply(a,b):	
	new_list = []
	for i in range(len(a)):
		value = a[i]*b[i]
		new_list.append(value)
	return new_list
#method to divide two lists
def list_divide(a,d):
	new_list = []
	for i in range(len(a)):
		value = a[i]/d
		new_list.append(value)
	return new_list

#node class stores data about each node
class node:
    def __init__(self,p,c,t):
        self.parent = p
        self.children = c
        self.node_type = t
        self.posteriors = []
        self.expected_value = 0
        self.decision=''
    #string representation of tree
    def __str__(self):
    	return 'Parent '+str(self.parent)+' Children '+str(self.children) + ' posteriors ' + str(self.posteriors) + 'nodeType ' + str(self.node_type) + ' eValue ' + str(self.expected_value) + ' decision ' + str(self.decision)
    #add a child to node, inputs are the node number of the child
    def add_child(self,node):
    	self.children.append(node)

#tree class implements tree 
class tree:
	def __init__(self):
		#intialize tree one root node with a survey or market node
		self.list_of_nodes=[]
		self.list_of_nodes.append(node([],[1,2],'root'))
		self.list_of_nodes.append(node(0,[],'market'))
		self.list_of_nodes.append(node(0,[],'survey'))
		self.list_of_nodes[2].posteriors=PRIORS
		self.list_of_nodes[1].posteriors=PRIORS
		self.string_representation=[]

	# method for adding nodes. Certain node types will have differnt posteriors based on the node before it's posteroir values
	def add_node(self,node):
		priors = self.node(node.parent).posteriors
		#update posteriors if the node is a survey result
		if (node.node_type in [0,1,2,3,4,5]):
			joint_probablity = list_multiply(priors,LIKELIHOODS[node.node_type])
			sum_joint = sum(joint_probablity)
			node.posteriors = list_divide(joint_probablity,sum_joint)
		#if not survey result then the posteroirs stay the same
		else:
			node.posteriors = priors
		# if there is an end node the expected value will equal the posteroirs multiplied by the revenue of each case
		if (node.node_type == 'end'):
			values = list_one_multiply(MARKETSHARES,MARKETVALUE)
			node.expected_value = sum(list_multiply(values,node.posteriors))

		self.list_of_nodes.append(node)
		self.list_of_nodes[node.parent].children.append(len(self.list_of_nodes)-1)
	#string represntation of the tree. prints out all nodes
	def __str__(self):
		for i in range(len(self.list_of_nodes)):
			self.string_representation.append([i,self.node(i).parent,self.node(i).children,self.node(i).posteriors,self.node(i).node_type,self.node(i).expected_value,self.node(i).decision])
		return str(self.string_representation)
	#export to csv
	def toCSV(self):
		with open("out.csv", "w", newline="") as f:
			writer = csv.writer(f)
			writer.writerows(self.string_representation)
	# returns a specific nod 
	def node(self,number):
		return self.list_of_nodes[number]
	#number of node in a tree
	def len(self):
		return(len(self.list_of_nodes))
	#returns the number of surveys done before the node, including that node
	def surveys_before(self,node):
		node_number=node
		surveys_before=0
		while(self.node(node_number).node_type != 'root'):
			if (self.node(node_number).node_type=='survey'):
				surveys_before +=1
			node_number=self.node(node_number).parent
		return surveys_before
	#changes the end values by subtracting the survey values of all the surveys done before
	def update_end_node_values(self):
		for i in reversed(range(self.len())):
			if (self.node(i).node_type == 'end'):
				self.node(i).expected_value -= self.surveys_before(i)*SURVEYCOST

	#method used to update expected values after tree is created quite complex because every type of node has a different script
	def update_expected_values(self):
		#use after placing end nodes
		for i in reversed(range(self.len())):
			#if node is end node there is no need to update expected values because the expected value was there there tree initialized
			if (self.node(i).node_type == 'end'):
				pass
			#if node is survey then the expected value will equal the probablities of each survey outcome multiplied by the expected value of each survey outcome
			elif(self.node(i).node_type == 'survey'):
				probablities = survey_outcome_odds(self.node(i).posteriors)
				expected_value=0
				#iterating through all the children of that node
				for k in range(6):
					nodek = self.child(i,k)
					expected_value=expected_value + (probablities[k] * nodek.expected_value)
				self.node(i).expected_value = expected_value
			#if node type is a survey outcome then the expected value will be the larger of the two of the next decision layer. Or if its an end node then it will equal the expected value of the end node
			elif(self.node(i).node_type in range(6)):
				if (self.child(i,0).node_type=='end'):
					self.node(i).expected_value = self.child(i,0).expected_value
				else:
					child1 = self.child(i,0)
					child2 = self.child(i,1)
					if(child1.expected_value>=child2.expected_value):
						self.node(i).decision = 'survey'
						self.node(i).expected_value = child1.expected_value
					else:
						self.node(i).expected_value = child2.expected_value
						self.node(i).decision = 'market'
			# if the node is a market node then it will equal the expected value of the end node
			elif(self.node(i).node_type == 'market'):
				child = self.child(i,0)
				self.node(i).expected_value = child.expected_value
	def child(self,i,k):
		#returns kth the child node for node i
		return self.list_of_nodes[self.list_of_nodes[i].children[k]]

#methods used to add layers to a tree. Can be a outcome or decision or end layer. Last layer must be an end layer
#why is this method not in the treee class, considering adding it to the tree class???
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

#example construction of tree
t = tree()
add_layer(t,'outcome')
add_layer(t,'decision')
add_layer(t,'outcome')
add_layer(t,'decision')
add_layer(t,'outcome')
add_layer(t,'end')
t.update_end_node_values()
t.update_expected_values()
print(t)
t.toCSV()




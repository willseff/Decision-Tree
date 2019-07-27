import numpy as np

LIKELIHOODS = [[0,0.4096,0.2592,0.0768,0.0064],[0,0.3,0.423,0.04,0.23],[0,123,0.84,0.001,0.3],[0,0.4096,0.2592,0.0768,0.0064],[0,0.4096,0.2592,0.0768,0.0064],[0,0.4096,0.2592,0.0768,0.0064]]
MARKETVALUE = 10000000
MARKETSHARES = [0,0.2,0.4,0.6,0.8]

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

    def __str__(self):
    	return 'Parent '+str(self.parent)+' Children '+str(self.children) + ' posteriors ' + str(self.posteriors) + 'nodeType ' + str(self.node_type) + ' eValue ' + str(self.expected_value)

    def add_child(self,node):
    	self.children.append(node)



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
add_layer(t,'end')
print(t)


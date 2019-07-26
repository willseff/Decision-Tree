class node:
    def __init__(self,p,c,t):

        self.parent = p
        self.children = c
        self.node_type = t
        self.priors = []
        self.posterors = []

    def __str__(self):
    	return 'Parent '+str(self.parent)+' Children '+str(self.children)

    def add_child(self,node):
    	self.children.append(node)



class tree:
	def __init__(self):
		self.list_of_nodes=[]
		self.list_of_nodes.append(node([],[1,2],'root'))
		self.list_of_nodes.append(node([0],[],'market'))
		self.list_of_nodes.append(node([0],[],'survey'))


	def add_node(self,node):
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

t = tree()


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

				

add_layer(t,'outcome')
add_layer(t,'decision')
add_layer(t,'outcome')
add_layer(t, 'decision')
add_layer(t,'outcome')
add_layer(t, 'decision')
add_layer(t,'outcome')
add_layer(t, 'decision')
print(t)

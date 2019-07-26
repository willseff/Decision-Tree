class node:
    def __init__(self,p,c,t):

        self.parent = p
        self.children = c
        self.node_type = t

    def __str__(self):
    	return 'Parent '+str(self.parent)+' Children '+str(self.children)

    def add_child(self,node):
    	self.children.append(node)


class tree:
	def __init__(self):
		self.list_of_nodes=[]
		self.list_of_nodes.append(node([],[],'survey'))

	def add_node(node):
		self.list_of_nodes.append(node)

	def get_node(self,number):
		return self.list_of_nodes[number]

	def len(self):
		return(len(self.list_of_nodes))

t = tree()
n= node([0],[2,3,4,5],'survey')


def add_layer(tree,layer_type):
	if(layer_type == 'survey'):
		for i in range(tree.len())
			if tree.get_node(i)








class Node:
	def __init__(self, identifier):
		self.identifier = identifier
		self.children = []

	@property
	def identifier(self):
		return self.identifier

	@property
	def children(self):
		return self.children


	def add_child(self, identifier):
		self.children.append(identifier)




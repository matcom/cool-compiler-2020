

class NameMap:
	def __init__(self, parent=None):
		self.namemap = {}
		self.parent = parent

	def define_variable(self, coolname, cilname):
		self.namemap[coolname] = cilname

	def create_child_scope(self):
		child_scope = NameMap(self)
		return child_scope

	def exit_child_scope(self):
		self.namemap = self.parent.namemap
		self.parent = self.parent.parent

	def get_cil_name(self, coolname):
		if not coolname in self.namemap.keys():
			return self.parent.get_cil_name(coolname) if self.parent else None
		else:
			return self.namemap[coolname]
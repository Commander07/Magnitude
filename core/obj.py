from . import id


class entity:
  def __init__(self, name, parent=None):
    self.id = id.getId()
    self.name = name
    self.childs = []
    self.parent = parent

  def add_child(self, child):
    child.parent = self
    self.childs.append(child)

  def __repr__(self):
    return f"{self.id},{self.name},{self.childs},{self.parent}"


class scene:
  def __init__(self, name="Untitled scene"):
    self.id = id.getId()
    self.name = name
    self.entity_list = []
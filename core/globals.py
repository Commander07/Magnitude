from . import obj
## TEST
te1 = obj.entity("Test entity 1")
te2 = obj.entity("Test entity 2")
te3 = obj.entity("Test entity 3")
te4 = obj.entity("Test entity 4")
te5 = obj.entity("Test entity 5")
te1.add_child(te4)
te1.add_child(te2)
te2.add_child(te3)
## DEFAULT SCENE
default_scene = obj.scene(name="default_scene")
default_scene.entity_list = [te1, te2, te3, te4, te5]
## OTHER
scenes = {"default_scene":default_scene}
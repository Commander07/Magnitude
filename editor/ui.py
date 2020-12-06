from dearpygui.core import *
from dearpygui.simple import *
from pyperclip import copy as pyperclip_copy
from yaml import load,dump,Loader

from core import globals
from core import obj

class console_log:
  def __init__(self):
    self.console_text = []
  def AddLog(self,text):
    self.console_text.append(str(text))
    add_text(str(text),parent="scrolling")
def save_layout(sender, data):
  ## TODO: add docking support;  use relative size and positsions
  windows = get_windows()
  l=open("editor/layout.yml","w")
  data = []
  for win in windows:
    win_ = get_item_configuration(win)
    data.append(win_)
    print("Name:",win_["name"],"x_pos:",win_["x_pos"],"y_pos:",win_["y_pos"],"width:",win_["width"],"height:",win_["height"])
  dump(data,l)
def load_layout():
  ## TODO: add docking support;  use relative size and positsions
  data=load(open("editor/layout.yml"),Loader=Loader)
  if data is None:return
  for item in data:
    name = item["name"]
    configure_item(name,**item)
current_scene = "default_scene"
cl = console_log()
def print_me(sender, data):
  log_debug(f"Menu Item: {sender}")
def open_proj(sender, data):
  ## TODO: serializer
  open_file_dialog(extensions=".me_project,.me_scene")
def theme_callback(sender, data):
  set_theme(sender)
def console_callback(sender, data):
  ## TODO: log things nicely;  create vm;  auto select after enter
  log_debug(sender)
  if sender == "Clear##console_clear":
    log_debug("clear")
  elif sender == "Copy##console_copy":
    pyperclip_copy("\n".join(cl.console_text))
  elif sender == "##console_command":
    value = get_value("##console_command")
    log_debug(value)
    set_value("##console_command","")
    cl.AddLog(eval(value))
def show_console(sender, data):
  configure_item("Magnitude Console v1.0.0##console",show=True)
def show_hierarchy(sender, data):
  configure_item("Hierarchy##hierarchy",show=True)
def show_inspector(sender, data):
  configure_item("Inspector##inspector",show=True)
def create_entity(sender, data):
  globals.scenes[current_scene].entity_list.append(obj.entity("Unnamed entity"))
  new_entity_hierarchy(globals.scenes[current_scene].entity_list[-1:][0])
def new_entity_hierarchy(ent,parent="entities##hierarchy_list"):
  ## TODO: fix leaf=True styles
  if ent.parent != None:
    add_indent(parent=ent.parent.name+"##"+ent.parent.id)
    add_indent(parent=ent.parent.name+"##"+ent.parent.id)
    if ent.childs == []: leaf=True
    else: leaf=False
    with collapsing_header(ent.name+"##"+ent.id,label=ent.name,parent=ent.parent.name+"##"+ent.parent.id,leaf=leaf):
      pass
    unindent(parent=ent.parent.name+"##"+ent.parent.id)
    unindent(parent=ent.parent.name+"##"+ent.parent.id)
  else:
    if ent.childs == []: leaf=True
    else: leaf=False
    with collapsing_header(ent.name+"##"+ent.id,label=ent.name,parent=parent,leaf=leaf):
      pass

with window("Main Window",no_title_bar=True,x_pos=0,y_pos=0,no_close=True,no_collapse=True):
  with menu_bar("Main Menu Bar"):
    with menu("File"):
      ## TODO: make all items function
      add_menu_item("Open", callback=open_proj)
      add_menu_item("Save", callback=save_layout)
      add_menu_item("Save As", callback=print_me)
    with menu("Themes"):
      add_menu_item("Dark", callback=theme_callback)
      add_menu_item("Light", callback=theme_callback)
      add_menu_item("Classic", callback=theme_callback)
      add_menu_item("Dark 2", callback=theme_callback)
      add_menu_item("Grey", callback=theme_callback)
      add_menu_item("Dark Grey", callback=theme_callback)
      add_menu_item("Cherry", callback=theme_callback)
      add_menu_item("Purple", callback=theme_callback)
      add_menu_item("Gold", callback=theme_callback)
      add_menu_item("Red", callback=theme_callback)
    with menu("View"):
      add_menu_item("Show Logger", callback=show_logger)
      add_menu_item("Show About", callback=show_about)
      add_menu_item("Show Metrics", callback=show_metrics)
      add_menu_item("Show Documentation", callback=show_documentation)
      add_menu_item("Show Debug", callback=show_debug)
      add_menu_item("Show Console", callback=show_console)
      add_menu_item("Show Hierarchy", callback=show_hierarchy)
      add_menu_item("Show Inspector", callback=show_inspector)
with window("Hierarchy##hierarchy"):
  ## TODO: add abillity to move entities
  with menu_bar("Hierarchy_options"):
    with menu("Create"):
      add_menu_item("Entity", callback=create_entity)
  with child("entities##hierarchy_list",border=False,autosize_x=True,autosize_y=True):
    for entity in globals.scenes[current_scene].entity_list:
      new_entity_hierarchy(entity)

with window("Inspector##inspector"):
  add_text("Inspector")
with window("Magnitude Console v1.0.0##console",width=500,height=500,x_pos=200,y_pos=200):
  ## TODO: make Auto-scroll work;  fix height issue
  AutoScroll = True
  loglevel = 1
  Filter = None
  add_button("Options##console_options",callback=console_callback,popup="Console options popup")
  add_same_line()
  add_button("Clear##console_clear",callback=console_callback)
  add_same_line()
  add_button("Copy##console_copy",callback=console_callback)
  add_same_line()
  add_input_text("Filter")
  add_separator()
  with popup("Options##console_options", "Console options popup", mousebutton=0):
    add_checkbox("Auto-scroll",default_value=True)
  with child("scrolling",border=False,horizontal_scrollbar=True,autosize_x=True,autosize_y=True):
    for t in cl.console_text:
      add_text(str(t))
  add_input_text("##console_command",callback=console_callback,hint="Command...",on_enter=True)

def start():
  ## TODO: set icon to ../assets/logo.png;  fix docking with primary window;  add custom title bar;  add docking layouts
  set_theme("Cherry")
  set_vsync(True)
  enable_docking(shift_only=False,dock_space=True)
  load_layout()
  set_main_window_title("Magnitude Editor")
  start_dearpygui()
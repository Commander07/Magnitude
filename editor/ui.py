import dearpygui.core as dpg
import dearpygui.simple as dpgs
from pyperclip import copy as pyperclip_copy
from yaml import load, dump, Loader
from os import path

from core import globals
from core import obj


class console_log:

  def __init__(self):
    self.console_text = []

  def AddLog(self, text):
    self.console_text.append(str(text))
    dpg.add_text(str(text), parent="scrolling")


def save_layout(sender, data):
  ## TODO: add docking support;  use relative size and positsions
  windows = dpg.get_windows()
  layout=open("editor/layout.yml", "w")
  data = []
  for win in windows:
    win_ = dpg.get_item_configuration(win)
    data.append(win_)
    print("Name:", win_["name"], "x_pos:", win_["x_pos"], "y_pos:", win_["y_pos"], "width:", win_["width"], "height:", win_["height"])
  dump(data, layout)


def load_layout():
  ## TODO: add docking support;  use relative size and positsions
  data=load(open("editor/layout.yml"), Loader=Loader)
  if data is None: return
  for item in data:
    name = item["name"]
    dpg.configure_item(name, **item)


current_scene = "default_scene"
cl = console_log()


def print_me(sender, data):
  dpg.log_debug(f"Menu Item: {sender}")


def open_proj(sender, data):
  ## TODO: serializer
  dpg.open_file_dialog(extensions=".me_project,.me_scene")


def save_file(sender, data):
  path_ = path.join(data[0], data[1])
  dpg.set_value("save_file_location", path_)
  data_ = open(path_, "w")
  data_.write("")


def save_proj(sender, data):
  ## TODO: serializer
  if sender == "Save As":
    dpg.open_file_dialog(extensions=".me_project,.me_scene", callback=save_file)
  else:
    data_ = open(dpg.get_value("save_file_location"), "w")
    data_.write("")


def theme_callback(sender, data):
  dpg.set_theme(sender)


def console_callback(sender, data):
  ## TODO: log things nicely;  create vm;  auto select after enter
  dpg.log_debug(sender)
  if sender == "Clear##console_clear":
    dpg.log_debug("clear")
  elif sender == "Copy##console_copy":
    pyperclip_copy("\n".join(cl.console_text))
  elif sender == "##console_command":
    value = dpg.get_value("##console_command")
    dpg.log_debug(value)
    dpg.set_value("##console_command", "")
    cl.AddLog(eval(value))


def show_console(sender, data):
  dpg.configure_item("Magnitude Console v1.0.0##console", show=True)


def show_hierarchy(sender, data):
  dpg.configure_item("Hierarchy##hierarchy", show=True)


def show_inspector(sender, data):
  dpg.configure_item("Inspector##inspector", show=True)


def create_entity(sender, data):
  globals.scenes[current_scene].entity_list.append(obj.entity("Unnamed entity"))
  new_entity_hierarchy(globals.scenes[current_scene].entity_list[-1:][0])


def new_entity_hierarchy(ent, parent="entities##hierarchy_list"):
  if ent.parent is not None:
    dpg.add_indent(parent=ent.parent.name + "##" + ent.parent.id)
    dpg.add_indent(parent=ent.parent.name + "##" + ent.parent.id)
    if ent.childs == []: bullet=True
    else: bullet=False
    with dpgs.collapsing_header(ent.name + "##" + ent.id, label=ent.name, parent=ent.parent.name + "##" + ent.parent.id, bullet=bullet):
      pass
    dpg.unindent(parent=ent.parent.name + "##" + ent.parent.id)
    dpg.unindent(parent=ent.parent.name + "##"+ ent.parent.id)
  else:
    if ent.childs == []: bullet=True
    else: bullet=False
    with dpgs.collapsing_header(ent.name + "##" + ent.id, label=ent.name, parent=parent, bullet=bullet):
      pass


with dpgs.window("Main Window", no_title_bar=True, x_pos=0, y_pos=0, no_close=True, no_collapse=True):
  with dpgs.menu_bar("Main Menu Bar"):
    with dpgs.menu("File"):
      ## TODO: make all items function
      dpg.add_menu_item("Open", callback=open_proj)
      dpg.add_menu_item("Save", callback=save_proj)
      dpg.add_menu_item("Save As", callback=save_proj)

    with dpgs.menu("Themes"):
      dpg.add_menu_item("Dark", callback=theme_callback)
      dpg.add_menu_item("Light", callback=theme_callback)
      dpg.add_menu_item("Classic", callback=theme_callback)
      dpg.add_menu_item("Dark 2", callback=theme_callback)
      dpg.add_menu_item("Grey", callback=theme_callback)
      dpg.add_menu_item("Dark Grey", callback=theme_callback)
      dpg.add_menu_item("Cherry", callback=theme_callback)
      dpg.add_menu_item("Purple", callback=theme_callback)
      dpg.add_menu_item("Gold", callback=theme_callback)
      dpg.add_menu_item("Red", callback=theme_callback)

    with dpgs.menu("View"):
      dpg.add_menu_item("Show Logger", callback=dpg.show_logger)
      dpg.add_menu_item("Show About", callback=dpgs.show_about)
      dpg.add_menu_item("Show Metrics", callback=dpgs.show_metrics)
      dpg.add_menu_item("Show Documentation", callback=dpgs.show_documentation)
      dpg.add_menu_item("Show Debug", callback=dpgs.show_debug)
      dpg.add_menu_item("Show Console", callback=show_console)
      dpg.add_menu_item("Show Hierarchy", callback=show_hierarchy)
      dpg.add_menu_item("Show Inspector", callback=show_inspector)


with dpgs.window("Hierarchy##hierarchy"):
  ## TODO: add abillity to move entities

  with dpgs.menu_bar("Hierarchy_options"):
    with dpgs.menu("Create"):
      dpg.add_menu_item("Entity", callback=create_entity)

  with dpgs.child("entities##hierarchy_list", border=False, autosize_x=True, autosize_y=True):
    for entity in globals.scenes[current_scene].entity_list:
      new_entity_hierarchy(entity)


with dpgs.window("Inspector##inspector"):
  dpg.add_text("Inspector")


with dpgs.window("Magnitude Console v1.0.0##console", width=500, height=500, x_pos=200, y_pos=200):
  ## TODO: make Auto-scroll work;  fix height issue
  AutoScroll = True
  loglevel = 1
  Filter = None
  dpg.add_button("Options##console_options", callback=console_callback, popup="Console options popup")
  dpg.add_same_line()
  dpg.add_button("Clear##console_clear", callback=console_callback)
  dpg.add_same_line()
  dpg.add_button("Copy##console_copy", callback=console_callback)
  dpg.add_same_line()
  dpg.add_input_text("Filter")
  dpg.add_separator()

  with dpgs.popup("Options##console_options", "Console options popup", mousebutton=0):
    dpg.add_checkbox("Auto-scroll", default_value=True)

  with dpgs.child("scrolling", border=False, horizontal_scrollbar=True, autosize_x=True, autosize_y=True):
    for t in cl.console_text:
      dpg.add_text(str(t))

  dpg.add_input_text("##console_command", callback=console_callback, hint="Command...", on_enter=True)


def start():
  ## TODO: set icon to ../assets/logo.png;  fix docking with primary window;  add custom title bar;  add docking layouts
  dpg.set_theme("Cherry")
  dpg.set_vsync(True)
  dpg.enable_docking(shift_only=False, dock_space=True)
  load_layout()
  dpg.set_main_window_title("Magnitude Editor")
  dpg.start_dearpygui()

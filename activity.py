#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gtk
import pygame

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import StopButton

from gettext import gettext as _

import sugargame.canvas
import conozco

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.build_toolbar()
        self.actividad = conozco.Conozco()
        self.build_canvas()
        self.show_all()

        


    def build_canvas(self):

        self.table = gtk.Table(1, 2, False)

        self.box1 = gtk.HBox()
        self.box1.set_size_request(350, 350)
        
        self.box1.set_border_width(5)
        self.box1.show()

        box = gtk.VBox()
        img = gtk.Image()
        img.set_from_file("activity/fua-icon.svg")
        img.show()
        box.add(img)

        self.box2 = gtk.HBox()
        self.box2.set_size_request(200, 200)
        self.box2.show()

        self.table.attach(self.box1, 0, 1, 0, 1)
        self.table.attach(box, 1, 2, 0, 1)
        self.set_canvas(self.table)
     
        
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.box1.add(self._pygamecanvas)
        
        #self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        self._pygamecanvas.run_pygame(self.actividad.principal)

        


    def build_toolbar(self):

        self.max_participants = 1

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass


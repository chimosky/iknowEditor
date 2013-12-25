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
from sugar.graphics.objectchooser import ObjectChooser

from gettext import gettext as _

import sugargame.canvas
import conozco
from points_list import Data

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.init_vars()
        self.build_toolbar()
        self.actividad = conozco.Conozco(self)
        self.build_canvas()
        self.run_canvas()
        self.show_all()

    def init_vars(self):
        self._image = None



    def build_toolbar(self):

        self.max_participants = 1

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # new pic button
        new_game = ToolButton('new-pic')
        new_game.connect('clicked', self._new_picture)
        new_game.set_tooltip(_('New picture'))
        toolbar_box.toolbar.insert(new_game, -1)

        # add / remove point buttons
        add_point = ToolButton("row-insert")
        add_point.connect("clicked", self._add_point)
        add_point.set_tooltip(_("Add a point"))
        toolbar_box.toolbar.insert(add_point, -1)

        rem_point = ToolButton("row-remove")
        rem_point.connect("clicked", self._remove_point)
        rem_point.set_tooltip(_("Remove the selected point"))
        toolbar_box.toolbar.insert(rem_point, -1)

        # separator and stop button
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def build_canvas(self):

        self.table = gtk.Table(1, 2, False)

        self.box1 = gtk.HBox()
        self.box1.set_size_request(350, 350)
        self.box1.show()

        self.box2 = gtk.HBox()
        self.box2.set_size_request(50, 200)
        self.box2.show()

        self.table.attach(self.box1, 0, 1, 0, 1)
        self.table.attach(self.box2, 1, 2, 0, 1)
        
        
        self.labels_and_values = Data(self)

        self.labels_and_values.connect("label-changed", self._label_changed)
        self.labels_and_values.connect("value-changed", self._value_changed)

        self.box2.add(self.labels_and_values)

        self.set_canvas(self.table)


    def run_canvas(self):
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.box1.add(self._pygamecanvas)

        self._pygamecanvas.grab_focus()
        self._pygamecanvas.run_pygame(self.actividad.principal)



    def _new_picture(self, widget):
        try:
            chooser = ObjectChooser(parent=self)
        except:
            chooser = None
        f = None
        if chooser is not None:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                dsobject = chooser.get_selected_object()
                f = dsobject.file_path
        if f is not None:
            self._image = pygame.image.load(f)
            self.actividad.set_background(self._image)


    def _add_point(self, widget, label="", value="City"):
        pos = self.labels_and_values.add_value(label, value)

    def _remove_point(self, widget):
        path = self.labels_and_values.remove_selected_value()
        self._update_points()

    def _add_coor(self, pos):
        if self._image is not None:
            self.labels_and_values.update_selected_value(pos)

    def _label_changed(self, treeview, path, new_label):
        self._update_points()

    def _value_changed(self, treeview, path, new_value):
        self._update_points()

    def _update_points(self):
        l = self.labels_and_values.get_info()
        self.actividad.update_points(l)



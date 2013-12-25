
import gtk
import gobject

from gettext import gettext as _

class Data(gtk.TreeView):

    __gsignals__ = {
             'some-changed': (gobject.SIGNAL_RUN_FIRST, None, [str, str], ), }
             

    def __init__(self, activity):

        gtk.TreeView.__init__(self)

        self.model = gtk.ListStore(str, str, str, str)
        self.set_model(self.model)

        # Label column

        column = gtk.TreeViewColumn(_("Position"))
        label = gtk.CellRendererText()
        label.set_property('editable', True)
        label.connect("edited", self._label_changed, self.model)

        column.pack_start(label)
        column.set_attributes(label, text=0)
        self.append_column(column)

        # Value column

        column = gtk.TreeViewColumn(_("Name"))
        value = gtk.CellRendererText()
        value.set_property('editable', True)
        value.connect("edited", self._value_changed, self.model)

        column.pack_start(value)
        column.set_attributes(value, text=1)
        column.set_expand(True)
        self.append_column(column)

        # dx column

        column = gtk.TreeViewColumn(_("dx"))
        value = gtk.CellRendererText()
        value.set_property('editable', True)
        value.connect("edited", self._dx_changed, self.model)

        column.pack_start(value)
        column.set_attributes(value, text=2)
        self.append_column(column)

        # dy column

        column = gtk.TreeViewColumn(_("dy"))
        value = gtk.CellRendererText()
        value.set_property('editable', True)
        value.connect("edited", self._dy_changed, self.model)

        column.pack_start(value)
        column.set_attributes(value, text=3)
        self.append_column(column)
        self.set_enable_search(False)

        self.show_all()

    def add_value(self, label, value, dx, dy):
        selected = self.get_selection().get_selected()[1]
        if not selected:
            path = 0

        elif selected:
            path = self.model.get_path(selected)[0] + 1

        iter = self.model.insert(path, [label, value, dx, dy])

        self.set_cursor(self.model.get_path(iter),
                        self.get_column(1),
                        True)

        return path

    def remove_selected_value(self):
        path, column = self.get_cursor()
        if path is not None:
            path = path[0]
            model, iter = self.get_selection().get_selected()
            self.model.remove(iter)
        return path

    def update_selected_value(self, data):
        path, column = self.get_cursor()
        if path is not None:
            path = path[0]
            self.model[path][0] = data
            self.emit("some-changed", str(path), data)

    def _label_changed(self, cell, path, new_text, model):
        model[path][0] = new_text
        self.emit("some-changed", str(path), new_text)

    def _value_changed(self, cell, path, new_text, model):
        model[path][1] = new_text
        self.emit("some-changed", str(path), new_text)

    def _dx_changed(self, cell, path, new_text, model):
        model[path][2] = new_text
        self.emit("some-changed", str(path), new_text)

    def _dy_changed(self, cell, path, new_text, model):
        model[path][3] = new_text
        self.emit("some-changed", str(path), new_text)

    def get_info(self):
        l = []
        for row in self.model:
            name = row[1]
            status, pos = self._validate_pos(row[0])
            dx = int(row[2])
            dy = int(row[3])
            if status:
                l.append((name, pos, dx, dy))
        return l

    def _validate_pos(self, pos):
        try:
            pos = pos.replace('(', '')
            pos = pos.replace(')', '')
            pos = pos.split(',')
            pos = [float(pos[0]), float(pos[1])]
            pos = (int(pos[0]), int(pos[1]))
        except Exception, err:
            print err
            return False, None
        return True, pos


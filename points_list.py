
import gtk
import gobject

from gettext import gettext as _

class Data(gtk.TreeView):

    __gsignals__ = {
             'label-changed': (gobject.SIGNAL_RUN_FIRST, None, [str, str], ),
             'value-changed': (gobject.SIGNAL_RUN_FIRST, None, [str, str], ), }

    def __init__(self, activity):

        gtk.TreeView.__init__(self)

        self.model = gtk.ListStore(str, str)
        self.set_model(self.model)

        # Label column

        column = gtk.TreeViewColumn(_("Label"))
        label = gtk.CellRendererText()
        label.set_property('editable', True)
        label.connect("edited", self._label_changed, self.model)

        column.pack_start(label)
        column.set_attributes(label, text=0)
        self.append_column(column)

        # Value column

        column = gtk.TreeViewColumn(_("Value"))
        value = gtk.CellRendererText()
        value.set_property('editable', True)
        value.connect("edited", self._value_changed, self.model, activity)

        column.pack_start(value)
        column.set_attributes(value, text=1)

        self.append_column(column)
        self.set_enable_search(False)

        self.show_all()

    def add_value(self, label, value):
        selected = self.get_selection().get_selected()[1]
        if not selected:
            path = 0

        elif selected:
            path = self.model.get_path(selected)[0] + 1

        iter = self.model.insert(path, [label, value])

        self.set_cursor(self.model.get_path(iter),
                        self.get_column(1),
                        True)



        return path

    def remove_selected_value(self):
        path, column = self.get_cursor()
        path = path[0]

        model, iter = self.get_selection().get_selected()
        self.model.remove(iter)

        return path

    def update_selected_value(self, data):
        path, column = self.get_cursor()
        path = path[0]
        self.model[path][0] = data
        #self.emit("label-changed", str(path), data)
        print 'remover', path, column

    def _label_changed(self, cell, path, new_text, model):


        model[path][0] = new_text

        self.emit("label-changed", str(path), new_text)

    def _value_changed(self, cell, path, new_text, model, activity):


        is_number = True
        number = new_text.replace(",", ".")
        try:
            float(number)
        except ValueError:
            is_number = False

        if is_number:
            decimals = utils.get_decimals(str(float(number)))
            new_text = locale.format('%.' + decimals + 'f', float(number))
            model[path][1] = str(new_text)

            self.emit("value-changed", str(path), number)

        elif not is_number:
            alert = Alert()

            alert.props.title = _('Invalid Value')
            alert.props.msg = \
                           _('The value must be a number (integer or decimal)')

            ok_icon = Icon(icon_name='dialog-ok')
            alert.add_button(gtk.RESPONSE_OK, _('Ok'), ok_icon)
            ok_icon.show()

            alert.connect('response', lambda a, r: activity.remove_alert(a))

            activity.add_alert(alert)

            alert.show()


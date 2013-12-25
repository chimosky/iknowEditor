#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import gettext as _


def save(l):
    f = open('salida.py', 'w')
    # encabezados
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("\n")
    f.write("from gettext import gettext as _\n")
    f.write("\n")
    f.write("CITIES = [\n")
    first = True
    for r in l:
        #    (_('name'), x, y, type, dx, dy),
        if first:
            first = False
        else:
            f.write(',\n')
        
        lin = "    (_('" + str(r[0]) + "'), " + str(r[1]) + ", " + str(r[2])
        lin = lin + ", 2, " + str(r[3]) + ", " + str(r[4]) + ")"

        f.write(lin)
    f.write('\n')
    f.write(']')
    f.close()

#!/usr/bin/env python
# encoding: utf-8

from gi.repository import GLib
from urllib.parse import unquote

import sys

import dbus
import dbus.service
import dbus.exceptions
import dbus.mainloop.glib

def decompose_uri(uri):
    """
    extract folder part & filename part.
    """
    last_slash = uri.rfind('/')
    uri_part   = uri[:last_slash]
    filename   = uri[last_slash + 1:]
    colon      = uri_part.find(':')
    folder     = uri_part[colon+3:]
    return (unquote(folder), unquote(filename))

def get_thunar_interface(bus):
    thunar_bus_name = 'org.xfce.FileManager'
    thunar_bus_path = '/org/xfce/FileManager'

    thunar_object = bus.get_object(thunar_bus_name, thunar_bus_path)
    thunar        = dbus.Interface(thunar_object, thunar_bus_name)

    return thunar

filemanager1_bus_name = 'org.freedesktop.FileManager1'
filemanager1_bus_path = '/org/freedesktop/FileManager1'

class FileManager1(dbus.service.Object):
    def __init__(self, session_bus, path):
        super().__init__(session_bus, path)
        self.thunar = get_thunar_interface(session_bus)

    @dbus.service.method(filemanager1_bus_name, in_signature='ass', out_signature='')
    def ShowItems(self, uris, startup_id):
        """
        handle `ShowItems' message, and forward to xfce4's filemanager
        """
        print('Got ShowItems message!')

        for uri in uris:
            parts = decompose_uri(uri)
            print('Will open folder `{}\', and select file `{}\'.'.format(parts[0], parts[1]))
            try:
                self.thunar.DisplayFolderAndSelect(parts[0], parts[1], '', '')
            except dbus.exceptions.DBusException as e:
                print(e)
                print("Caught DBusException, try renew thunar interface.")
                self.thunar = get_thunar_interface(dbus.SessionBus())
                try:
                    self.thunar.DisplayFolderAndSelect(parts[0], parts[1], '', '')
                except dbus.exceptions.DBusException as e:
                    print(e)
                    print("Another DBusException... good luck then.")
                    sys.exit(-1)
            except Exception as e:
                print(e)
                print("Don't know what to do then...")
                sys.exit(-2)

        print('Done.')

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    bus_name    = dbus.service.BusName(filemanager1_bus_name, session_bus)
    filemanager = FileManager1(session_bus, filemanager1_bus_path)

    print('Service started.')

    mainloop = GLib.MainLoop()
    mainloop.run()

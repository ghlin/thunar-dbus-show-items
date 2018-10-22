# thunar-dbus-show-items

A DBus service implements `org.freedesktop.FileManager1`'s `ShowItems` method (by forwarding the request to thunar).

With this service, "Open containing folder" from firefox opens thunar and select/highlight the downloaded file.

see also:

- [Downloads - File - Open Containing Folder doesn't highlight/select downloaded file in Thunar file manager (XFCE)](https://bugzilla.mozilla.org/show_bug.cgi?id=1037856)

- [dbus - request to implement showItems method](https://bugzilla.xfce.org/show_bug.cgi?id=11024)

## dependences

- urllib

- python-dbus

- python-gobject

#!/usr/bin/python3

import dbus
import sys
import random

item              = "org.freedesktop.Notifications"
path              = "/org/freedesktop/Notifications"
interface         = "org.freedesktop.Notifications"
app_name          = "houston_servicemenu" + str(random.random()) #random is used to don't group notifications
id_num_to_replace = 0
icon              = ""
title             = ""
text              = ""
actions_list      = ''
hint              = ''
time              = 0   # Use seconds x 1000

last_arg = None

for arg in sys.argv[1:]:
    if last_arg   == '--icon':
        icon  = arg
    elif last_arg == '--title':
        title = arg
    elif last_arg == '--text':
        text  = arg
    
    last_arg = arg
    

try:
    bus = dbus.SessionBus()
    notif = bus.get_object(item, path)
    notify = dbus.Interface(notif, interface)
    koko = notify.Notify(app_name, id_num_to_replace, icon, title, text, actions_list, hint, time)
except:
    sys.exit(1)

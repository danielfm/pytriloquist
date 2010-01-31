#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bluetooth import *
import subprocess

# Try to use pynotify to notify server events
try:
    import pynotify
    pynotify.init("Pytriloquist")
    PYNOTIFY = True
except ImportError:
    PYNOTIFY = False

# Mouse commands
MOUSE_MOVE  = 'xte "mousermove %s %s"' # x, y
MOUSE_CLICK = 'xte "mouseclick %s"'    # mouse button
MOUSE_DRAG  = 'xte "mousedown %s"'     # mouse button
MOUSE_DROP  = 'xte "mouseup %s"'       # mouse button


def notify(message, title="Pytriloquist", icon=None):
    """Displays a notification message.
    """
    if PYNOTIFY:
        pynotify.Notification(title, message, icon).show()
    else:
        print title + ":", message

def server_socket(channel):
    """Creates a Bluetooth RFCOMM server socket bound to the given channel.
    """
    socket = BluetoothSocket(proto=RFCOMM)
    socket.bind(("", channel))
    return socket

def mouse_move(data):
    """Moves the mouse pointer to a new coordinate 'x:y' relative to the current
    position.
    """
    run_command(MOUSE_MOVE % tuple(data.split(":")))

def mouse_click(data):
    """Clicks the a mouse button.
    """
    run_command(MOUSE_CLICK % data)

def mouse_drag(data):
    """Holds down a mouse button.
    """
    run_command(MOUSE_DRAG % data)

def mouse_drop(data):
    """Releases a mouse button.
    """
    run_command(MOUSE_DROP % data)

def run_command(cmd):
    """Runs a command.
    """
    subprocess.Popen(cmd, shell=True)

def main(*argv):
    """Main loop.
    """
    import optparse
    p = optparse.OptionParser()

    # Required command line options
    p.add_option("--channel"  , "-c", default="3", help="Bluetooth channel")
    options = p.parse_args()[0]

    dispatcher = [run_command, mouse_move, mouse_click, mouse_drag, mouse_drop]

    socket = server_socket(int(options.channel))
    socket.listen(1)

    while True:
        notify("Waiting for connections", icon="gtk-refresh")
        (client, addr) = socket.accept()

        try:
            cmd = None
            notify("%s connected" % addr[0], title="Connection accepted", icon="gtk-dialog-info")
            while True:
                data = client.recv(512)
                cmd_type = int(data[0])
                cmd = data[1:].split("\n")[0]
                dispatcher[cmd_type](cmd)
        except BluetoothError:
            notify("%s disconnected" % addr[0], title="Connection closed", icon="gtk-stop")
        except:
            notify("Unexpected error", icon="gtk-dialog-error")


if __name__ == "__main__":
    main()

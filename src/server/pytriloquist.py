#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bluetooth import *
import subprocess


# Mouse commands
MOUSE_MOVE  = 'xte "mousermove %s %s"' # x, y
MOUSE_CLICK = 'xte "mouseclick %s"'    # mouse button
MOUSE_DRAG  = 'xte "mousedown %s"'     # mouse button
MOUSE_DROP  = 'ste "mouseup %s"'       # mouse button


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
        print "Waiting for connections..."
        (client, addr) = socket.accept()

        try:
            cmd = None
            print "Accepted connection from " + addr[0]
            while True:
                data = client.recv(512)
                cmd_type = int(data[0])
                cmd = data[1:].split("\n")[0]
                dispatcher[cmd_type](cmd)
        except BluetoothError:
            print "Connection closed by peer"
        except:
            print "Unexpected error"


if __name__ == "__main__":
    main()

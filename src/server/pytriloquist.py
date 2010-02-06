#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bluetooth import *
import subprocess


class PytriloquistServer(object):
    """
    Pytriloquist server implementation.
    """
    def __init__(self, config):
        self.config = config

    def _notify_init(self):
        """Initializes the notification system.
        """
        self.pynotify = None
        if getattr(self.config, 'USE_PYNOTIFY', None):
            try:
                self.pynotify = __import__('pynotify', {}, {}, [''])
                self.pynotify.init("Pytriloquist Server")
            except:
                self.pynotify = None

    def notify(self, message, title="Pytriloquist", icon=None):
        """Displays a notification message on the server desktop.
        """
        if self.pynotify:
            self.pynotify.Notification(title, message, icon).show()
        else:
            print title + ":", message

    def _server_socket(self, channel):
        """Creates a Bluetooth RFCOMM server socket bound to the given channel.
        """
        socket = BluetoothSocket(proto=RFCOMM)
        socket.bind(("", channel))
        socket.listen(1)
        return socket

    def mouse_move(self, data):
        """Moves the mouse pointer to a new coordinate 'x:y' relative to the current
        position.
        """
        self.run_command(self.config.MOUSE_MOVE % tuple(data.split(":")))

    def mouse_click(self, data):
        """Clicks the a mouse button.
        """
        self.run_command(self.config.MOUSE_CLICK % data)

    def mouse_drag(self, data):
        """Holds down a mouse button.
        """
        self.run_command(self.config.MOUSE_DRAG % data)

    def mouse_drop(self, data):
        """Releases a mouse button.
        """
        self.run_command(self.config.MOUSE_DROP % data)

    def run_command(self, cmd):
        """Runs a command.
        """
        subprocess.Popen(cmd, shell=True)

    def start(self):
        """Starts the server.
        """
        self._notify_init()

        # Event dispatcher
        dispatcher = (
            self.run_command, self.mouse_move,
            self.mouse_click, self.mouse_drag, self.mouse_drop,
        )

        socket = self._server_socket(self.config.CHANNEL)
        while True:
            (client, addr) = socket.accept()

            # Ignore blacklisted devices
            if addr[0] not in self.config.ALLOWED_DEVICES:
                try:
                    client.close()
                except:
                    pass
                continue

            try:
                cmd = None
                self.notify("%s connected" % addr[0], title="Connection accepted", icon="gtk-dialog-info")
                while True:
                    data = client.recv(512)
                    cmd_type = int(data[0])
                    cmd = data[1:].split("\n")[0]
                    dispatcher[cmd_type](cmd)
            except BluetoothError:
                self.notify("%s disconnected" % addr[0], title="Connection closed", icon="gtk-stop")
            except:
                self.notify("Unexpected error", icon="gtk-dialog-error")


def parse_options():
    """Parses the command line options.
    """
    import optparse
    p = optparse.OptionParser()

    # Required command line options
    p.add_option("--config", "-c", default="config",
                 help="Configuration module name (e.g. mypackage.config)")
    options = p.parse_args()[0]

    # Configuration module
    return __import__(options.config, {}, {}, [''])


if __name__ == '__main__':
    config = parse_options()
    PytriloquistServer(config).start()

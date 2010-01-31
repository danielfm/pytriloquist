import btsocket as socket


# For deferred translation
_ = lambda s:s


class BluetoothClient(object):
    """Communication over Bluetooth.
    """
    def __init__(self, app):
        self.socket = None
        self.app = app

    def is_connected(self):
        """Returns whether the client is connected.
        """
        return self.socket != None

    def connect(self):
        """Connects to the server.
        """
        try:
            if not self.is_connected():
                server_addr = self.app.get_settings()[:2]
                self.socket = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
                self.socket.setblocking(False)
                self.socket.connect(server_addr)
        except:
            self.close()
            raise BluetoothError(_(u"Cannot connect."))

    def close(self):
        """Closes the connection.
        """
        try:
            if self.is_connected():
                self.socket.close()
        except:
            pass
        finally:
            self.socket = None

    def send_command(self, cmd_id, cmd):
        """Sends a command to the server.
        """
        if not self.is_connected():
            raise BluetoothError(_(u"Not connected."))
        try:
            self.socket.send(str(cmd_id) + cmd + "\n")
        except socket.error:
            raise BluetoothError(_(u"Communication error."))
        except:
            raise BluetoothError(_(u"Unexpected error."))


class BluetoothError(Exception):
    """
    Generic Bluetooth error.
    """
    def __init__(self, msg):
        self.msg = msg

import btsocket as socket
import appuifw as ui

class BluetoothClient(object):
    """Communication over Bluetooth.
    """
    def __init__(self, app):
        """
        """
        self.socket = None
        self.app = app

    def connect(self):
        """Connects to the server.
        """
        if not self.socket:
            settings = self.app.get_settings()
            self.socket = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
            self.socket.connect(settings[:2])

    def close(self):
        """Closes the connection.
        """
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
        except:
            pass

    def send_command(self, cmd_id, cmd):
        """Sends a command to the server.
        """
        self.connect()
        if self.socket:
            self.socket.send(str(cmd_id) + cmd + "\n")

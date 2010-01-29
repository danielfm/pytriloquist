import btsocket as socket
import appuifw as ui

class BluetoothClient(object):
    """Communication over Bluetooth.
    """
    def __init__(self, app):
        """Initializes a new instance.
        """
        self.socket = None
        self.app = app

    def connect(self):
        """Connects to the server.
        """
        try:
            if not self.socket:
                server_addr = self.app.get_settings()[:2]
                self.socket = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
                self.socket.connect(server_addr)
        except:
            self.close()
            raise

    def close(self):
        """Closes the connection.
        """
        try:
            if self.socket:
                self.socket.close()
        except:
            pass
        finally:
            self.socket = None

    def send_command(self, cmd_id, cmd):
        """Sends a command to the server.
        """
        self.connect()
        try:
            if self.socket:
                self.socket.send(str(cmd_id) + cmd + "\n")
        except:
            self.close()
            raise

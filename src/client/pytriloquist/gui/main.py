import appuifw as ui
import globalui

from pytriloquist import Const
from pytriloquist.btclient import BluetoothError

from pytriloquist.gui import Dialog
from pytriloquist.gui.settings import SettingsDialog
from pytriloquist.gui.app      import ApplicationsDialog
from pytriloquist.gui.input    import InputDialog


class MainDialog(Dialog):
    """
    This dialog displays the list of modes.
    """
    def __init__(self, app):
        Dialog.__init__(self, app)

    def get_title(self):
        """Returns the dialog title.
        """
        return Const.APP_TITLE

    def init_ui(self):
        """Initializes the user interface.
        """
        self.settings_dialog = SettingsDialog(self.app, self)
        self.apps_dialog     = ApplicationsDialog(self.app, self)

        # Tabs
        self.tabs = [
            (_(u"Apps"), self.open_apps),
        ]

        self.menu_connect    = (_(u"Connect"), self.connect)
        self.menu_disconnect = (_(u"Disconnect"), self.disconnect)

        # Only works with touch-enabled devices
        if ui.touch_enabled():
            self.input_dialog = InputDialog(self.app, self)
            self.tabs.append((_(u"Input"), self.open_input))

    def get_menu(self):
        """Gets the application menus.
        """
        connect = self.menu_connect
        if self.app.btclient.is_connected():
            connect = self.menu_disconnect

        return [
            connect,
            (_(u"Settings"), self.show_settings),
            (_(u"About")   , self.show_about),
            (_(u"Exit")    , self.app.exit),
        ]

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.screen = "normal"
        ui.app.set_tabs([t[0] for t in self.tabs], self.tab_handler)
        ui.app.exit_key_handler = self.app.exit
        self.tab_handler(0)

    def connect(self):
        """Connects to the server.
        """
        try:
            self.app.btclient.connect()
        except BluetoothError, e:
            ui.note(_(e.msg), "error")
        else:
            self.replace_menu(self.menu_connect, self.menu_disconnect)

    def disconnect(self):
        """Disconnects from the server.
        """
        try:
            self.app.btclient.close()
        except BluetoothError, e:
            ui.note(_(e.msg), "error")
        finally:
            self.replace_menu(self.menu_disconnect, self.menu_connect)

    def replace_menu(self, old, new):
        """Replaces a menu entry by another.
        """
        menu = ui.app.menu
        index = menu.index(old)
        if index >= 0:
            menu[index] = new
            ui.app.menu = menu

    def open_apps(self):
        """Opens the applications dialog.
        """
        self.apps_dialog.execute()

    def open_input(self):
        """Opens the input dialog.
        """
        if ui.touch_enabled():
            self.input_dialog.execute()
        else:
            ui.note(_(u"Touch not enabled."), "error")

    def tab_handler(self, index):
        """Handles tab events.
        """
        [t[1] for t in self.tabs][index]()

    def show_settings(self):
        """Shows the settings dialog.
        """
        self.settings_dialog.execute()

    def show_about(self):
        """Shows the about dialog.
        """
        data = {
            "title"  : Const.APP_TITLE,
            "version": Const.APP_VERSION,
            "year"   : Const.APP_YEAR,
            "url"    : Const.APP_URL,
            "author" : Const.APP_AUTHOR,
            "lauthor": _(u"Authors:"),
        }
        text = u"%(title)s v%(version)s (c) %(year)s\n" \
                "%(url)s\n\n"                           \
                "%(lauthor)s\n"                         \
                "%(author)s" % data
        globalui.global_msg_query(text, _(u"About"), 0)

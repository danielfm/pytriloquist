import appuifw as ui
import globalui

from pytriloquist import Const
from pytriloquist.btclient import BluetoothError

from pytriloquist.gui import Dialog
from pytriloquist.gui.settings import SettingsDialog
from pytriloquist.gui.app      import ApplicationsDialog
from pytriloquist.gui.input    import InputDialog


class IntroDialog(Dialog):
    """
    Application starting point.
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
        self.main_dialog     = MainDialog(self.app, self)
        self.settings_dialog = SettingsDialog(self.app, self)

        self.menu = [
            (_(u"Open") , self.opt_list_observe),
            (_(u"About"), self.about),
            (_(u"Exit") , self.app.exit),
        ]

        self.options = [
            (1, _("Connect") , self.connect),
            (2, _("Settings"), self.settings)
        ]
        self.opt_list = ui.Listbox([opt[1] for opt in self.options], self.opt_list_observe)

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.screen = "normal"
        ui.app.set_tabs([], None)
        ui.app.menu = self.menu
        ui.app.body = self.opt_list
        ui.app.exit_key_handler = self.app.exit

    def opt_list_observe(self):
        """Function called when a mode is selected from the list.
        """
        selected = self.options[self.opt_list.current()]
        selected[2]()

    def connect(self):
        """Connects to the server.
        """
        try:
            self.app.btclient.connect()
        except BluetoothError, e:
            ui.note(_(e.msg), "error")
        else:
            self.main_dialog.execute()

    def settings(self):
        """Opens the Settings dialog.
        """
        self.settings_dialog.execute()

    def about(self):
        """Opens the About dialog.
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


class MainDialog(Dialog):
    """
    This dialog displays the list of applications and input methods.
    """
    def __init__(self, app, parent):
        Dialog.__init__(self, app, parent)

    def get_title(self):
        """Returns the dialog title.
        """
        return Const.APP_TITLE

    def init_ui(self):
        """Initializes the user interface.
        """
        self.tabs = [
            (_(u"Apps"), self.open_apps),
        ]

        self.menu = [
            (_(u"Orientation"), (
                (_(u"Automatic"), self.set_orientation("automatic")),
                (_(u"Landscape"), self.set_orientation("landscape")),
                (_(u"Portrait") , self.set_orientation("portrait")),
            )),
            (_(u"Disconnect"), self.back)
        ]

        # Dialogs
        self.apps_dialog = ApplicationsDialog(self.app, self)
        if ui.touch_enabled():
            # Only works with touch-enabled devices
            self.input_dialog = InputDialog(self.app, self)
            self.tabs.append((_(u"Input"), self.open_input))

    def set_orientation(self, orientation):
        """Returns a function that changes the display orientation.
        """
        def fn():
            ui.app.orientation = orientation
        return fn

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.set_tabs([t[0] for t in self.tabs], self.tab_handler)
        ui.app.exit_key_handler = self.app.exit
        self.tab_handler(0)

    def back(self):
        """Executes the parent dialog.
        """
        Dialog.back(self)
        self.disconnect()

    def disconnect(self):
        """Disconnects from the server.
        """
        try:
            self.app.btclient.close()
        except BluetoothError, e:
            ui.note(_(e.msg), "error")

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

import appuifw as ui

from pytriloquist import Const
from pytriloquist.gui import Dialog


class SettingsDialog(Dialog):
    """
    Dialog used to configure the application.
    """
    def __init__(self, app, parent):
        """Initializes the dialog.
        """
        Dialog.__init__(self, app, parent)
        self.form_saved = False

    def get_title(self):
        """Returns the dialog title.
        """
        return _(u"Settings")

    def init_ui(self):
        """Initializes the user interface.
        """
        # List of available locales
        locales = [_(text) for text in Const.APP_LOCALES.values()]

        # Load settings
        settings = self.app.get_settings()

        device  = settings[0]
        channel = settings[1]
        locale  = Const.APP_LOCALES.keys().index(settings[2])

        # Form fields
        self.fields = [
            (_(u"Bluetooth Device"), "text"  , device),
            (_(u"Channel")         , "number", channel),
            (_(u"Language")        , "combo" , (locales, locale)),
        ]

        # Adjust flags
        self.initialized = True

        # Set up form
        self.form = ui.Form(self.fields, flags=ui.FFormEditModeOnly | ui.FFormDoubleSpaced)
        self.form.save_hook = self.save

    def display(self):
        """Displays the dialog on the device.
        """
        self.form_saved = False

        ui.app.set_tabs([], None)
        self.form.execute()
        self.parent.execute(force=self.form_saved)

    def get_bt_device(self):
        """Gets the bluetooth device address from the saved form.
        """
        if self.form_saved:
            return self.saved_data[0][2]

    def get_bt_channel(self):
        """Gets the bluetooth device channel from the saved form.
        """
        if self.form_saved:
            return self.saved_data[1][2]

    def get_locale(self):
        """Gets the locale from the saved form.
        """
        if self.form_saved:
            locales = Const.APP_LOCALES.keys()
            return locales[self.saved_data[2][2][1]]

    def save(self, data):
        """Stores the entered configuration data.
        """
        self.form_saved, self.saved_data = True, data

        # Save settings
        self.app.dbm.execute(Const.DB_SETTINGS_UPDATE % (
            self.get_bt_device(),
            self.get_bt_channel(),
            self.get_locale()
        ))

        # Update the locale and close the bluetooth connection, so the new
        # settings are used from now on
        self.app.set_locale(self.get_locale())
        self.app.btclient.close()

        return True

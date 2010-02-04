import gettext
import os

import appuifw as ui
import e32
import e32db
import globalui

import btclient
import db


class Const(object):
    """Constant data.
    """
    # Used for deferred translation
    _ = lambda text: text

    # Environment
    ENV_WORKING_DIR   = unicode(os.getcwd())
    ENV_WORKING_DRIVE = ENV_WORKING_DIR.split(u":")[0] + u":"

    # App data
    APP_TITLE   = u"Pytriloquist"
    APP_VERSION = u"0.2"
    APP_LOCALE  = u"en"
    APP_YEAR    = 2010
    APP_AUTHOR  = u"Daniel Fernandes Martins"
    APP_URL     = u"github.com/danielfm/pytriloquist"

    # Locales
    APP_LOCALES_DIR = ENV_WORKING_DIR + ur"\locale"
    APP_LOCALES = {
        "pt_BR": _(u"Portuguese (BR)"),
        "en"   : _(u"English"),
    }

    # Database tables
    DB_FILE               = ENV_WORKING_DRIVE + ur"\pytriloquist.db"
    DB_TABLE_APPLICATIONS = u"CREATE TABLE applications (id COUNTER, name VARCHAR)"
    DB_TABLE_COMMANDS     = u"CREATE TABLE commands (id COUNTER, app_id UNSIGNED INTEGER, name VARCHAR, command VARCHAR)"
    DB_TABLE_SETTINGS     = u"CREATE TABLE settings (id UNSIGNED INTEGER, device VARCHAR, channel UNSIGNED TINYINT, locale VARCHAR)"

    # Database SQLs
    DB_SETTINGS_UPDATE  = u"UPDATE settings SET device = '%s', channel = %d, locale = '%s'"
    DB_SETTINGS_SELECT  = u"SELECT device, channel, locale FROM settings"
    DB_SETTINGS_DEFAULT = u"INSERT INTO settings (device, channel, locale) VALUES ('AA:BB:CC:DD:EE:FF', 3, 'en')"

    DB_APPLICATIONS_SELECT = u"SELECT id, name FROM applications ORDER BY name ASC"
    DB_APPLICATIONS_INSERT = u"INSERT INTO applications (name) VALUES ('%s')"
    DB_APPLICATIONS_DELETE = u"DELETE FROM applications WHERE id = %d"
    DB_APPLICATIONS_UPDATE = u"UPDATE applications SET name = '%s' WHERE id = %d"

    DB_COMMANDS_SELECT     = u"SELECT id, app_id, name, command FROM commands WHERE app_id = %d ORDER BY name ASC"
    DB_COMMANDS_INSERT     = u"INSERT INTO commands (app_id, name, command) VALUES (%d, '%s', '%s')"
    DB_COMMANDS_DELETE     = u"DELETE FROM commands WHERE id = %d"
    DB_COMMANDS_APP_DELETE = u"DELETE FROM commands WHERE app_id = %d"
    DB_COMMANDS_UPDATE     = u"UPDATE commands SET name = '%s', command = '%s' WHERE id = %d"

    # Mouse commands
    MOUSE_MOVE          = "%s:%s" # (x, y) coordinate
    MOUSE_LEFT_BUTTON   = "1"
    MOUSE_MIDDLE_BUTTON = "2"
    MOUSE_RIGHT_BUTTON  = "3"
    MOUSE_SCROLL_DOWN   = "4"
    MOUSE_SCROLL_UP     = "5"
    MOUSE_SCROLL_LEFT   = "6"
    MOUSE_SCROLL_RIGHT  = "7"


class App(object):
    """
    Controls the application execution and global state.
    """
    def __init__(self):
        """Initializes the application.
        """
        self.lock     = e32.Ao_lock()
        self.btclient = btclient.BluetoothClient(self)
        self.dbm      = db.DBManager(Const.DB_FILE)
        self._open_db()
        self.set_locale()

    def get_title(self):
        """Gets the application title.
        """
        return ui.app.title

    def set_title(self, title=Const.APP_TITLE):
        """Sets the application title.
        """
        ui.app.title = title

    def set_locale(self, locale=None):
        """Sets the current locale. Is no locale is given, it uses the
        default one.
        """
        translation_dir = Const.APP_LOCALES_DIR

        # Load locale from settings
        settings = self.get_settings()
        locale = settings[2]

        # Use the default locale otherwise
        if locale not in Const.APP_LOCALES:
            locale = Const.APP_LOCALE

        # Set the current locale
        t = gettext.translation("pytriloquist", translation_dir, [locale])
        t.install(unicode=True)
        self.locale = locale

    def get_locale(self):
        """Gets the current locale.
        """
        return self.locale

    def _open_db(self):
        """Opens the app database. Create the database if it doesn't exist.
        """
        if self.dbm.open_or_create():
            self.dbm.execute_atomic([
                Const.DB_TABLE_APPLICATIONS,
                Const.DB_TABLE_COMMANDS,
                Const.DB_TABLE_SETTINGS,
                Const.DB_SETTINGS_DEFAULT,
            ])

    def get_settings(self):
        """Get the application settings from the database.
        """
        view = self.dbm.query(Const.DB_SETTINGS_SELECT)
        view.get_line()
        return tuple([view.col(i+1) for i in range(view.col_count())])

    def run(self, dialog):
        """Runs the application.
        """
        dialog.execute()
        self.lock.wait()

    def exit(self):
        """Closes the application.
        """
        ui.app.set_tabs([], None)
        self.btclient.close()
        self.dbm.close()
        self.lock.signal()

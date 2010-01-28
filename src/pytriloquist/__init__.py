import gettext

import appuifw as ui
import e32
import e32db
import globalui

import btclient
import db


class Const(object):
    """Constant data.
    """
    table_applications = u"CREATE TABLE applications (id COUNTER, name VARCHAR)"
    table_commands     = u"CREATE TABLE commands (id COUNTER, app_id UNSIGNED INTEGER, name VARCHAR, command VARCHAR)"
    table_settings     = u"CREATE TABLE settings (id UNSIGNED INTEGER, device VARCHAR, channel UNSIGNED TINYINT, locale VARCHAR)"

    settings_update  = u"UPDATE settings SET device = '%s', channel = %d, locale = '%s'"
    settings_select  = u"SELECT device, channel, locale FROM settings"
    settings_default = u"INSERT INTO settings (device, channel, locale) VALUES ('AA:BB:CC:DD:EE:FF', 3, 'pt_BR')"

    apps_select = u"SELECT id, name FROM applications ORDER BY name ASC"
    apps_insert = u"INSERT INTO applications (name) VALUES ('%s')"
    apps_delete = u"DELETE FROM applications WHERE id = %d"
    apps_rename = u"UPDATE applications SET name = '%s' WHERE id = %d"

    cmds_select     = u"SELECT id, app_id, name, command FROM commands WHERE app_id = %d ORDER BY name ASC"
    cmds_insert     = u"INSERT INTO commands (app_id, name, command) VALUES (%d, '%s', '%s')"
    cmds_delete     = u"DELETE FROM commands WHERE id = %d"
    cmds_app_delete = u"DELETE FROM commands WHERE app_id = %d"
    cmds_edit       = u"UPDATE commands SET name = '%s', command = '%s' WHERE id = %d"


class App(object):
    """
    Controls the application execution and global state.
    """
    def __init__(self):
        """Initializes the application.
        """
        self.lock     = e32.Ao_lock()
        self.btclient = btclient.BluetoothClient(self)
        self.dbm      = db.DBManager(self.get_meta()["db_file"])
        self._open_or_create_db()
        self.set_locale()


    def get_meta(self):
        """Gets the application metadata.
        """
        # Deferred translation
        _ = lambda text: text

        return {
            "title"  : u"Pytriloquist",
            "version": u"0.1",
            "year"   : u"2010",
            "url"    : u"github.com/danielfm/pytriloquist",

            "loc" : "en",
            "locs": {
                "pt_BR": _(u"Portuguese (BR)"),
                "en"   : _(u"English"),
            },
            "db_file" : ur"e:\data\pytriloquist\preferences.db",
            "locs_dir": ur"e:\data\pytriloquist\locale",
        }

    def get_title(self):
        """Gets the application title.
        """
        return ui.app.title

    def set_title(self, title=None):
        """Sets the application title.
        """
        if not title:
            title = self.get_meta()["title"]
        ui.app.title = title

    def set_locale(self, locale=None):
        """Sets the current locale. Is no locale is given, it uses the
        default one.
        """
        translation_dir = self.get_meta()["locs_dir"]

        # Load locale from settings
        settings = self.get_settings()
        locale = settings[2]

        # Use the default locale otherwise
        if locale not in self.get_meta()["locs"]:
            locale = self.get_meta()["loc"]

        # Set the current locale
        t = gettext.translation("pytriloquist", translation_dir, [locale])
        t.install(unicode=True)
        self.locale = locale

    def get_locale(self):
        """Gets the current locale.
        """
        return self.locale

    def _open_or_create_db(self):
        """
        """
        if self.dbm.open_or_create():
            self.dbm.execute_atomic([
                Const.table_applications,
                Const.table_commands,
                Const.table_settings,
                Const.settings_default
            ])

    def get_settings(self):
        """Get the application settings from the database.
        """
        view = self.dbm.query(Const.settings_select)
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

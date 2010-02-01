import appuifw as ui

from pytriloquist import Const
from pytriloquist.btclient import BluetoothError
from pytriloquist.gui import Dialog


class ApplicationsDialog(Dialog):
    """
    Dialog used to manage applications.
    """
    def __init__(self, app, parent):
        Dialog.__init__(self, app, parent)

    def get_title(self):
        """Returns the dialog title.
        """
        return self.parent.get_title()

    def init_ui(self):
        """Initializes the user interface.
        """
        # Load the list of applications
        self.apps = []
        view = self.app.dbm.query(Const.DB_APPLICATIONS_SELECT)
        for i in range(view.count_line()):
            view.get_line()
            self.apps.append((view.col(1), view.col(2)))
            view.next_line()

        # Menu
        self.menu = [
            (_(u"New")   , self.new_app),
            (_(u"Delete"), self.delete_app),
            (_(u"Rename"), self.rename_app),
        ]
        self.menu.extend(self.parent.menu)

        # Cannot display an empty Listbox
        if not self.apps:
            self.apps.append((-1, _("New")))
        self.app_list = ui.Listbox([app[1] for app in self.apps], self.app_list_observe)

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.body = self.app_list
        ui.app.menu = self.menu

    def app_list_observe(self):
        """Function called when an application is selected from the list.
        """
        selected = self.apps[self.app_list.current()]
        if selected[0] == -1:
            self.new_app()
        else:
            CommandsDialog(selected, self.app, self).execute()

    def new_app(self):
        """Adds a new application.
        """
        name = ui.query(_(u"Application name"), "text")
        if name:
            self.app.dbm.execute(Const.DB_APPLICATIONS_INSERT % name)
            self.execute(force=True)

    def delete_app(self):
        """Removes the selected application.
        """
        index = self.app_list.current()
        if index >= 0:
            selected = self.apps[index]
            if selected[0] >= 0:
                if ui.query(_(u"Delete \"%s\"?") % selected[1], "query"):
                    self.app.dbm.execute_atomic([
                        Const.DB_APPLICATIONS_DELETE % selected[0],
                        Const.DB_COMMANDS_APP_DELETE % selected[0]])
                    self.execute(force=True)
            else:
                ui.note(_(u"Cannot remove an action."), "error")

    def rename_app(self):
        """Renames the selected application.
        """
        index = self.app_list.current()
        if index >= 0:
            selected = self.apps[index]
            if selected[0] >= 0:
                name = ui.query(_(u"Application name"), "text", self.apps[index][1])
                if name:
                    self.app.dbm.execute(
                        Const.DB_APPLICATIONS_UPDATE % (name, selected[0]))
                    self.execute(force=True)
            else:
                ui.note(_(u"Cannot edit an action."), "error")


class CommandsDialog(Dialog):
    """
    Dialog used to manage the commands of an application.
    """
    def __init__(self, app_data, app, parent):
        Dialog.__init__(self, app, parent)
        self.app_data = app_data

    def get_title(self):
        """Returns the dialog title.
        """
        return self.app_data[1]

    def init_ui(self):
        """Initializes the user interface.
        """
        # Load the list of commands
        self.cmds = []

        view = self.app.dbm.query(Const.DB_COMMANDS_SELECT % self.app_data[0])
        for i in range(view.count_line()):
            view.get_line()
            self.cmds.append((view.col(1), view.col(2), view.col(3), view.col(4)))
            view.next_line()

        # Menu
        self.menu = [
            (_(u"New")   , self.new_cmd),
            (_(u"Delete"), self.delete_cmd),
            (_(u"Edit")  , self.edit_cmd),
            (_(u"Back")  , self.back),
        ]

        # Cannot display an empty Listbox
        if not self.cmds:
            self.cmds.append((-1, -1, _("New"), ""))

        self.cmd_list = ui.Listbox([cmd[2] for cmd in self.cmds], self.cmd_list_observe)

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.body = self.cmd_list
        ui.app.menu = self.menu

    def cmd_list_observe(self):
        """Function called when a command is selected from the list.
        """
        selected = self.cmds[self.cmd_list.current()]
        if selected[0] == -1:
            self.new_cmd()
        else:
            try:
                self.app.btclient.send_command(0, selected[3])
            except BluetoothError, e:
                ui.note(_(e.msg), "error")

    def new_cmd(self):
        """Adds a new command.
        """
        EditCommandDialog(self.app_data, None, self.app, self).execute()

    def delete_cmd(self):
        """Removes the selected command.
        """
        index = self.cmd_list.current()
        if index >= 0:
            selected = self.cmds[index]
            if selected[0] >= 0:
                if ui.query(_(u"Delete \"%s\"?") % selected[2], "query"):
                    self.app.dbm.execute(Const.DB_COMMANDS_DELETE % selected[0])
                    self.execute(force=True)
            else:
                ui.note(_(u"Cannot remove an action."), "error")

    def edit_cmd(self):
        """Renames the selected command.
        """
        index = self.cmd_list.current()
        if index >= 0:
            selected = self.cmds[index]
            if selected[0] >= 0:
                EditCommandDialog(self.app_data, selected, self.app, self).execute()
            else:
                ui.note(_(u"Cannot edit an action."), "error")


class EditCommandDialog(Dialog):
    """
    Dialog used to add and edit application commands.
    """
    def __init__(self, app_data, command_data, app, parent):
        Dialog.__init__(self, app, parent)
        self.form_saved   = False
        self.app_data     = app_data
        self.command_data = command_data

    def get_title(self):
        """Returns the dialog title.
        """
        return self.app_data[1]

    def init_ui(self):
        """Initializes the user interface.
        """
        name    = u""
        command = u""

        if self.command_data:
            name    = self.command_data[2]
            command = self.command_data[3]

        # Form fields
        self.fields = [
            (_(u"Command name"), "text", name),
            (_(u"Command line"), "text", command),
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
        self.form.execute()
        self.parent.execute(force=self.form_saved)

    def get_name(self):
        """Gets the command name from the saved form.
        """
        if self.form_saved:
            return self.saved_data[0][2]

    def get_command(self):
        """Gets the command line from the saved form.
        """
        if self.form_saved:
            return self.saved_data[1][2]

    def save(self, data):
        """Adds or edits the command.
        """
        self.form_saved, self.saved_data = True, data

        if not self.command_data:
            self.app.dbm.execute(Const.DB_COMMANDS_INSERT % (
                self.app_data[0],
                self.get_name(),
                self.get_command()
            ))
        else:
            self.app.dbm.execute(Const.DB_COMMANDS_UPDATE % (
                self.get_name(),
                self.get_command(),
                self.command_data[0]
            ))

        return True

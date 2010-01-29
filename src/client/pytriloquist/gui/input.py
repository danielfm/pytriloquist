import appuifw as ui
import btsocket as socket
import key_codes

from pytriloquist import Const, gui


class InputDialog(gui.Dialog):
    """
    Dialog used to send input commands.
    """
    def __init__(self, app, parent):
        """Initializes the dialog.
        """
        gui.Dialog.__init__(self, app, parent)
        self.old_x = self.old_y = 0

    def get_title(self):
        """Returns the dialog title.
        """
        return self.parent.get_title()

    def init_ui(self):
        """Initializes the user interface.
        """
        self.canvas = ui.Canvas(event_callback=self.event, redraw_callback=self.redraw, resize_callback=self.resize)

        self.size = self.canvas.size
        self.width, self.height = self.size

        self.btn_size     = 60
        self.gap_size     = 10
        self.scroll_width = 30

        # Menu callbacks
        self.menu = self.parent.menu

    def display(self):
        """Displays the dialog on the device.
        """
        ui.app.directional_pad = False
        ui.app.body = self.canvas
        ui.app.menu = self.menu

        self.redraw(None)

    def left_mouse_button(self):
        """Defines the location of the left mouse button on the screen.
        """
        # Button box
        btn_left_x1 = self.gap_size
        btn_left_y1 = self.height - self.btn_size - self.gap_size

        btn_left_x2 = btn_left_x1 + self.btn_size
        btn_left_y2 = btn_left_y1 + self.btn_size

        self.btn_left_box = [(btn_left_x1, btn_left_y1), (btn_left_x2, btn_left_y2)]

    def draw_left_mouse_button(self):
        """Draws the left mouse button.
        """
        self.canvas.rectangle(self.btn_left_box, 0x000000, None)

        # Button text
        btn_left = _(u"L")
        btn_left_txt = self.canvas.measure_text(btn_left, font="title")[0]
        btn_left_txt_width  = btn_left_txt[2] - btn_left_txt[0]
        btn_left_txt_height = btn_left_txt[3] - btn_left_txt[1]

        btn_left_txt_x = self.btn_left_box[0][0] + self.btn_size/2 - btn_left_txt_width/2
        btn_left_txt_y = self.btn_left_box[0][1] + self.btn_size/2 + btn_left_txt_height/2
        self.canvas.text((btn_left_txt_x, btn_left_txt_y), btn_left, font="title")

    def right_mouse_button(self):
        """Defines the location of the right mouse button on the screen.
        """
        btn_right_x1 = self.btn_size + self.gap_size * 2
        btn_right_y1 = self.height - self.btn_size - self.gap_size

        btn_right_x2 = btn_right_x1 + self.btn_size
        btn_right_y2 = btn_right_y1 + self.btn_size

        self.btn_right_box = [(btn_right_x1, btn_right_y1), (btn_right_x2, btn_right_y2)]

    def draw_right_mouse_button(self):
        """Draws the right mouse button.
        """
        self.canvas.rectangle(self.btn_right_box, 0x000000, None)

        # Button text
        btn_right = _(u"R")
        btn_right_txt = self.canvas.measure_text(btn_right, font="title")[0]
        btn_right_txt_width  = btn_right_txt[2] - btn_right_txt[0]
        btn_right_txt_height = btn_right_txt[3] - btn_right_txt[1]

        btn_right_txt_x = self.btn_right_box[0][0] + self.btn_size/2 - btn_right_txt_width/2
        btn_right_txt_y = self.btn_right_box[0][1] + self.btn_size/2 + btn_right_txt_height/2
        self.canvas.text((btn_right_txt_x, btn_right_txt_y), btn_right, font="title")

    def vert_scroll(self):
        """Defines the location of the vertical scroll on the screen.
        """
        vert_scroll_x1 = self.width - self.gap_size - self.scroll_width
        vert_scroll_y1 = self.gap_size

        vert_scroll_x2 = self.width - self.gap_size
        vert_scroll_y2 = self.height - self.gap_size - self.scroll_width
        self.vert_scroll_box = [(vert_scroll_x1, vert_scroll_y1), (vert_scroll_x2, vert_scroll_y2)]

    def draw_vert_scroll(self):
        """Draws the vertical scroll.
        """
        self.canvas.rectangle(self.vert_scroll_box, None, 0xeeeeee);

    def horiz_scroll(self):
        """Defines the location of the horizontal scroll on the screen.
        """
        horiz_scroll_x1 = self.btn_right_box[1][0] + self.gap_size
        horiz_scroll_y1 = self.height - self.gap_size - self.scroll_width

        horiz_scroll_x2 = self.width - self.gap_size - self.scroll_width
        horiz_scroll_y2 = self.height - self.gap_size
        self.horiz_scroll_box = [(horiz_scroll_x1, horiz_scroll_y1), (horiz_scroll_x2, horiz_scroll_y2)]

    def draw_horiz_scroll(self):
        """Draws the horizontal scroll.
        """
        self.canvas.rectangle(self.horiz_scroll_box, None, 0xeeeeee);

    def draw_touchpad(self):
        """Draws the touchpad background.
        """
        self.canvas.clear()

        touchpad     = _(u"Touchpad")
        touchpad_txt = self.canvas.measure_text(touchpad, font="title")[0]

        touchpad_txt_width  = touchpad_txt[2] - touchpad_txt[0]
        touchpad_txt_height = touchpad_txt[3] - touchpad_txt[1]

        touchpad_txt_x = self.width/2 - touchpad_txt_width/2
        touchpad_txt_y = self.height/2 + touchpad_txt_height/2
        self.canvas.text((touchpad_txt_x, touchpad_txt_y), touchpad, font="title", fill=0xbbbbbb)

    def place_components(self):
        """Places the components on the screen.
        """
        self.left_mouse_button()
        self.right_mouse_button()
        self.vert_scroll()
        self.horiz_scroll()

    def draw_components(self):
        """Draw the components on the screen.
        """
        self.draw_touchpad()
        self.draw_left_mouse_button()
        self.draw_right_mouse_button()
        self.draw_vert_scroll()
        self.draw_horiz_scroll()

    def redraw(self, rect):
        """Canvas redraw callback.
        """
        self.place_components()
        self.draw_components()        

    def resize(self, wh):
        """Canvas resize callback.
        """
        self.width, self.height = wh
        try:
            self.redraw([(0, 0), wh])
        except:
            pass

    def is_inside(self, rect, point):
        """Returns whether point is inside rect.
        """
        x, y = point
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        return x >= x1 and x <= x2 and y >= y1 and y <= y2

    def send_command(self, cmd_type, cmd):
        """Sends a Bluetooth command to the server.
        """
        try:
            self.app.btclient.send_command(cmd_type, cmd)
        except socket.error:
            ui.note(_(u"Communication failed."), 'error')
        except:
            ui.note(_(u"Unexpected error."), 'error')

    def handle_click(self, x, y):
        """Handles the mouse click.
        """
        self.left_clicking   = False
        self.right_clicking  = False
        self.moving          = False
        self.vert_scrolling  = False
        self.horiz_scrolling = False

        if self.is_inside(self.btn_left_box, (x, y)):
            self.left_clicking = True
        elif self.is_inside(self.btn_right_box, (x, y)):
            self.right_clicking = True
        elif self.is_inside(self.vert_scroll_box, (x, y)):
            self.vert_scrolling = True
        elif self.is_inside(self.horiz_scroll_box, (x, y)):
            self.horiz_scrolling = True
        else:
            self.moving = True
            self.old_x, self.old_y = x, y

    def handle_move(self, x, y):
        """Handles the mouse move.
        """
        delta_xy = (x-self.old_x, y-self.old_y)
        self.old_x, self.old_y = x, y
        self.send_command(1, Const.MOUSE_MOVE % delta_xy)

    def handle_vert_scroll(self, y):
        """Handles the mouse vertical scroll.
        """
        delta_y = y - self.old_y
        self.old_y = y
        if delta_y < 0:
            self.send_command(2, Const.MOUSE_SCROLL_DOWN)
        elif delta_y > 0:
            self.send_command(2, Const.MOUSE_SCROLL_UP)

    def handle_horiz_scroll(self, x):
        """Handles the mouse horizontal scroll.
        """
        delta_x = x - self.old_x
        self.old_x = x
        if delta_x < 0:
            self.send_command(2, Const.MOUSE_SCROLL_LEFT)
        elif delta_x > 0:
            self.send_command(2, Const.MOUSE_SCROLL_RIGHT)

    def handle_release(self, x, y):
        """Handles the mouse release.
        """
        # Left click or drag gesture
        if self.left_clicking:
            if self.is_inside(self.btn_left_box, (x, y)):
                self.send_command(2, Const.MOUSE_LEFT_BUTTON)
            else:
                self.send_command(3, Const.MOUSE_LEFT_BUTTON)

        # Right click or drag gesture
        if self.right_clicking:
            if self.is_inside(self.btn_right_box, (x, y)):
                self.send_command(2, Const.MOUSE_RIGHT_BUTTON)
            else:
                self.send_command(3, Const.MOUSE_RIGHT_BUTTON)

    def event(self, event):
        """Canvas event callback.
        """
        x, y = 0, 0

        # Only handle these events
        if not event['type'] in [key_codes.EButton1Up, key_codes.EButton1Down, key_codes.EDrag]:
            return

        # Current x,y coordinate
        if 'pos' in event:
            x, y = event['pos']

        # Screen touched
        if event['type'] == key_codes.EButton1Down:
            self.handle_click(x, y)

        # Moving mouse pointer
        if self.moving and event['type'] == key_codes.EDrag:
            self.handle_move(x, y)

        # Using the vertical scroll bar
        if self.vert_scrolling and event['type'] == key_codes.EDrag:
            self.handle_vert_scroll(y)

        # Using the horizontal scroll bar
        if self.horiz_scrolling and event['type'] == key_codes.EDrag:
            self.handle_horiz_scroll(x)

        # Finished touch gesture
        if event['type'] == key_codes.EButton1Up:
            self.handle_release(x, y)

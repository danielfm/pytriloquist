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

        # Canvas size
        self.width, self.height = self.canvas.size

        # Size of each component
        self.btn_size     = 60
        self.gap_size     = 10
        self.scroll_width = 30

        # State associated with screen rects
        self.event_rect = {
            'moving'         : None,
            'left_clicking'  : lambda: self.btn_left_box,
            'middle_clicking': lambda: self.btn_middle_box,
            'right_clicking' : lambda: self.btn_right_box,
            'vert_scrolling' : lambda: self.vert_scroll_box,
            'horiz_scrolling': lambda: self.horiz_scroll_box,
        }

        # Keeps the mouse button used in dragging or zero
        self.dragging = 0

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
        self.draw_box(self.btn_left_box, _(u"L"))

    def middle_mouse_button(self):
        """Defines the location of the middle mouse button on the screen.
        """
        btn_middle_x1 = self.btn_left_box[1][0] + self.gap_size/2
        btn_middle_y1 = self.btn_left_box[0][1]

        btn_middle_x2 = btn_middle_x1 + self.btn_size/2
        btn_middle_y2 = btn_middle_y1 + self.btn_size

        self.btn_middle_box = [(btn_middle_x1, btn_middle_y1), (btn_middle_x2, btn_middle_y2)]

    def draw_middle_mouse_button(self):
        """Draws the middle mouse button.
        """
        self.draw_box(self.btn_middle_box, _(u"M"), font=None)

    def right_mouse_button(self):
        """Defines the location of the right mouse button on the screen.
        """
        btn_right_x1 = self.btn_middle_box[1][0] + self.gap_size/2
        btn_right_y1 = self.btn_middle_box[0][1]

        btn_right_x2 = btn_right_x1 + self.btn_size
        btn_right_y2 = btn_right_y1 + self.btn_size

        self.btn_right_box = [(btn_right_x1, btn_right_y1), (btn_right_x2, btn_right_y2)]

    def draw_right_mouse_button(self):
        """Draws the right mouse button.
        """
        self.draw_box(self.btn_right_box, _(u"R"))

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
        box = [(0, 0), (self.width, self.height)]
        self.draw_box(box, _("Touchpad"), fill=0xbbbbbb, border=None, bg=0xffffff)

    def draw_box(self, rect, text, font="title", fill=0x000000, border=0x000000, bg=None):
        """Draw a button.
        """
        self.canvas.rectangle(rect, border, bg)

        btn_txt = self.canvas.measure_text(text, font=font)[0]
        btn_txt_width  = btn_txt[2] - btn_txt[0]
        btn_txt_height = btn_txt[3] - btn_txt[1]

        width  = rect[1][0] - rect[0][0]
        height = rect[1][1] - rect[0][1]

        btn_txt_x = rect[0][0] + width/2 - btn_txt_width/2
        btn_txt_y = rect[0][1] + height/2 + btn_txt_height/2
        self.canvas.text((btn_txt_x, btn_txt_y), text, fill=fill, font=font)

    def place_components(self):
        """Places the components on the screen.
        """
        self.left_mouse_button()
        self.middle_mouse_button()
        self.right_mouse_button()
        self.vert_scroll()
        self.horiz_scroll()

    def draw_components(self):
        """Draw the components on the screen.
        """
        self.draw_touchpad()
        self.draw_left_mouse_button()
        self.draw_middle_mouse_button()
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

    def reset_state_vars(self):
        """Resets touchpad state.
        """
        for state in self.event_rect.keys():
            setattr(self, state, False)

    def handle_click(self, x, y):
        """Handles the mouse click.
        """
        self.reset_state_vars()
        for state, rect_fn in self.event_rect.items():
            if rect_fn and self.is_inside(rect_fn(), (x, y)):
                setattr(self, state, True)
                break
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
        button_state = [
            (self.left_clicking  , Const.MOUSE_LEFT_BUTTON  , self.btn_left_box),
            (self.middle_clicking, Const.MOUSE_MIDDLE_BUTTON, self.btn_middle_box),
            (self.right_clicking , Const.MOUSE_RIGHT_BUTTON , self.btn_right_box),
        ]

        for button, box in [s[1:] for s in button_state if s[0]]:
            if self.is_inside(box, (x, y)):
                if self.dragging:
                    old_button = self.dragging
                    self.dragging = 0
                    self.send_command(4, old_button)
                self.send_command(2, button)
            else:
                self.dragging = button
                self.send_command(3, button)

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

        # Dragging
        if event['type'] == key_codes.EDrag:
            if self.moving:
                self.handle_move(x, y)
            elif self.vert_scrolling:
                self.handle_vert_scroll(y)
            elif self.horiz_scrolling:
                self.handle_horiz_scroll(x)

        # Finished touch gesture
        if event['type'] == key_codes.EButton1Up:
            self.handle_release(x, y)

import sys

sys.path.append('E:/data/python')

from pytriloquist import App
from pytriloquist.gui.main import MainDialog

# Main loop
if __name__ == '__main__':
    app  = App()
    main = MainDialog(app)
    app.run(main)

from pytriloquist import App
from pytriloquist.gui.main import IntroDialog

# Main loop
if __name__ == '__main__':
    app  = App()
    main = IntroDialog(app)
    app.run(main)

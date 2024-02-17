if __name__ == '__main__':
    import os, sys

    if getattr(sys, 'frozen', False):
        ROOT_PATH = sys._MEIPASS
    else:
        ROOT_PATH = os.path.dirname(__file__)
    os.chdir(os.path.split(ROOT_PATH)[0])

    if not os.path.exists(f"data"):
        os.makedirs(f"data")

    from gui import start_gui

    import import_previous
    import_previous.import_previous()

    start_gui.start()

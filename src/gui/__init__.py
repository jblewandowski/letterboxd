from tkinter import Tk
import sys
from .config import colors, page_hierarchy

root = Tk()
root.title("Jake's Letterboxd Data Visualizer")
# root.tk.call('tk', 'scaling', 2.0)/
root.protocol('WM_DELETE_WINDOW', sys.exit)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

if screen_width > screen_height:
    window_width = int(screen_height / 2 * 4 / 3)
    window_height = int(screen_height / 2)
else:
    window_width = int(screen_width / 2)
    window_height = int(screen_width / 8 * 3)

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.configure(bg=colors['bg'])

import global_data
global_data.root = root

from .page_creator import pagecreator
pagecreator(root, page_hierarchy)
